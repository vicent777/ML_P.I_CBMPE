import pandas as pd
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)


def transform_ocorrencias(df: pd.DataFrame, save_artifacts: bool = False) -> pd.DataFrame:
    df = df.copy()

    # Conversão dataHoraChamada
    df["data"] = df["dataHoraChamada"].dt.date
    df["hora"] = df["dataHoraChamada"].dt.hour
    df["dia_semana"] = df["dataHoraChamada"].dt.dayofweek
    df["mes"] = df["dataHoraChamada"].dt.month
    df["ano"] = df["dataHoraChamada"].dt.year
    df["fim_de_semana"] = df["dia_semana"].isin([5, 6]).astype(int)

    # Padronização statusAtendimento
    df["statusAtendimento"] = (
        df["statusAtendimento"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df["atendida"] = (df["statusAtendimento"] == "atendida").astype(int)

    # Padronização formaAcionamento
    df["formaAcionamento"] = (
        df["formaAcionamento"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Turno
    def definir_turno(h):
        if 6 <= h < 12:
            return "manha"
        elif 12 <= h < 18:
            return "tarde"
        elif 18 <= h < 24:
            return "noite"
        else:
            return "madrugada"

    df["turno"] = df["hora"].apply(definir_turno)

    # Padronização município
    df["municipio"] = (
        df["municipio"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # 🔹 Encoding por frequência (FEATURE DEPENDENTE DO DATASET)
    freq_municipio = df["municipio"].value_counts(normalize=True)
    df["municipio_freq"] = df["municipio"].map(freq_municipio)

    if save_artifacts:
        freq_municipio.to_json(ARTIFACTS_DIR / "freq_municipio.json")

    # Drop colunas não usadas
    colunas_drop = [
        "statusAtendimento",
        "formaAcionamento",
    ]

    df = df.drop(columns=colunas_drop, errors="ignore")

    return df
