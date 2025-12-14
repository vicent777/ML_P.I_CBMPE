from fastapi import FastAPI, Query
import joblib
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Carrega modelo e features
model = joblib.load("models/xgb_ocorrencias_diario.pkl")
features_template = joblib.load("models/features_modelo.pkl")

# Configurações do banco a partir de variáveis de ambiente
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT")
}

def get_ocorrencias_diarias(municipio: str, data: str):
    """Retorna ocorrencias diarias de municipio até a data fornecida."""
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
    """Gera todas as features que o modelo espera."""
    data_dt = datetime.strptime(data, "%Y-%m-%d")
    
    # Filtro para datas anteriores
    df['data'] = pd.to_datetime(df['data'])
    df = df[df['data'] <= data_dt]

    # Ocorrencias do dia anterior
    dia_anterior = data_dt - timedelta(days=1)
    ocorrencias_dia_anterior = int(df[df['data'] == dia_anterior]['qtd_ocorrencias'].sum() if not df[df['data'] == dia_anterior].empty else 0)

    # Ocorrencias da semana anterior (mesmo dia da semana)
    semana_anterior = data_dt - timedelta(days=7)
    ocorrencias_semana_anterior = int(df[df['data'] == semana_anterior]['qtd_ocorrencias'].sum() if not df[df['data'] == semana_anterior].empty else 0)

    # Média móvel 7 dias
    df_sorted = df.sort_values('data')
    df_sorted['media_movel_7_dias'] = df_sorted['qtd_ocorrencias'].rolling(7, min_periods=1).mean()
    media_movel_7_dias = df_sorted[df_sorted['data'] == data_dt]['media_movel_7_dias'].values[0] if not df_sorted[df_sorted['data'] == data_dt].empty else 0

    # Fim de semana
    fim_de_semana = 1 if data_dt.weekday() >= 5 else 0  # 5=sabado, 6=domingo

    # Dia da semana e mês
    dia_semana = data_dt.weekday()
    mes = data_dt.month

    # Municipio freq (dummy ou frequência relativa)
    municipio_freq = 1.0  # simplificação, pode ajustar se tiver encoding real

    # Monta DataFrame final com a ordem das features
    data_dict = {
        "municipio_freq": municipio_freq,
        "media_movel_7_dias": media_movel_7_dias,
        "ocorrencias_dia_anterior": ocorrencias_dia_anterior,
        "ocorrencias_semana_anterior": ocorrencias_semana_anterior,
        "fim_de_semana": fim_de_semana,
        "dia_semana": dia_semana,
        "mes": mes,
    }

    df_features = pd.DataFrame([data_dict])
    df_features = df_features[features_template]  # Garante a mesma ordem
    return df_features

@app.get("/previsao")
def previsao(municipio: str = Query(...), data: str = Query(...)):
    df_ocorrencias = get_ocorrencias_diarias(municipio, data)
    
    if df_ocorrencias.empty:
        return {"municipio": municipio, "data": data, "previsao": 0}
    
    df_features = gerar_features(df_ocorrencias, municipio, data)
    pred = model.predict(df_features)
    return {"municipio": municipio, "data": data, "previsao": int(pred[0])}
