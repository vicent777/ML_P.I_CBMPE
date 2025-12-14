from fastapi import FastAPI, Query
import joblib
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import os
import numpy as np 
from dotenv import load_dotenv
from src.pipelines.transformacao_ocorrencias import transform_ocorrencias

load_dotenv()

app = FastAPI()
freq_municipio = pd.read_json("artifacts/freq_municipio.json", typ="series")

# Carrega modelo e features
model = joblib.load("models/xgb_ocorrencias_diario.pkl")
features_template = joblib.load("models/features_modelo.pkl")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT")
}

def get_ocorrencias_diarias(municipio: str, data: str):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT data, municipio, qtd_ocorrencias
        FROM ocorrencias_diarias
        WHERE municipio = %s AND data <= %s
        ORDER BY data
    """
    cursor.execute(query, (municipio, data))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(rows)

def gerar_features(df: pd.DataFrame, municipio: str, data: str):
    data_dt = datetime.strptime(data, "%Y-%m-%d")

    df = df.copy()
    df["data"] = pd.to_datetime(df["data"])
    df = df[df["data"] < data_dt]  # 🔥 usa apenas passado

    df = df.sort_values("data")

    df["media_movel_7_dias"] = (
        df["qtd_ocorrencias"]
        .rolling(7, min_periods=1)
        .mean()
    )

    media_movel_7_dias = float(df["media_movel_7_dias"].iloc[-1]) if not df.empty else 0.0

    ocorrencias_dia_anterior = (
        int(df.iloc[-1]["qtd_ocorrencias"]) if len(df) >= 1 else 0
    )

    ocorrencias_semana_anterior = (
        int(df.iloc[-7]["qtd_ocorrencias"]) if len(df) >= 7 else 0
    )

    fim_de_semana = 1 if data_dt.weekday() >= 5 else 0

    data_dict = {
        "municipio_freq": float(freq_municipio.get(municipio, 0.0)),
        "media_movel_7_dias": media_movel_7_dias,
        "ocorrencias_dia_anterior": ocorrencias_dia_anterior,
        "ocorrencias_semana_anterior": ocorrencias_semana_anterior,
        "fim_de_semana": fim_de_semana,
        "dia_semana": data_dt.weekday(),
        "mes": data_dt.month,
    }

    df_features = pd.DataFrame([data_dict])
    return df_features[features_template]

@app.get("/previsao")
def previsao(
    municipio: str = Query(...),
    data_inicio: str = Query(...),
    dias: int = Query(7)
):
    municipio = municipio.strip().lower()
    df_hist = get_ocorrencias_diarias(municipio, data_inicio)

    if df_hist.empty:
        return {"erro": "Sem histórico suficiente"}

    df_hist["data"] = pd.to_datetime(df_hist["data"])
    df_hist = df_hist.sort_values("data")

    preds = []

    # ✅ começa a prever a partir do DIA SEGUINTE
    data_atual = datetime.strptime(data_inicio, "%Y-%m-%d") + timedelta(days=1)

    for _ in range(dias):
        X = gerar_features(df_hist, municipio, data_atual.strftime("%Y-%m-%d"))

        pred_log = model.predict(X)[0]
        pred_real = float(max(0.0, np.expm1(pred_log)))

        preds.append({
            "data": data_atual.strftime("%Y-%m-%d"),
            "previsao": float(round(pred_real, 2))
        })

        df_hist = pd.concat([
            df_hist,
            pd.DataFrame([{
                "data": data_atual,
                "municipio": municipio,
                "qtd_ocorrencias": pred_real
            }])
        ], ignore_index=True)

        data_atual += timedelta(days=1)

    return {
        "municipio": municipio,
        "previsoes": preds
    }
