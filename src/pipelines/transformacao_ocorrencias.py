import pandas as pd

def transform_ocorrencias(df):

    df = df.copy()

    # Conversão dataHoraChamada
    df["data"] = df["dataHoraChamada"].dt.date
    df["hora"] = df["dataHoraChamada"].dt.hour
    df["dia_semana"] = df["dataHoraChamada"].dt.dayofweek
    df["mes"] = df["dataHoraChamada"].dt.month
    df["ano"] = df["dataHoraChamada"].dt.year
    df["fim_de_semana"] = df["dia_semana"].isin([5, 6]).astype(int)


    # Padronização statusAtendimento e criação variável atendida
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

    # Criação variável turno
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


    # Padronização de município
    df["municipio"] = (
        df["municipio"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Encoding por frequência
    freq_municipio = df["municipio"].value_counts(normalize=True)
    df["municipio_freq"] = df["municipio"].map(freq_municipio)

    colunas_drop = [
        "statusAtendimento",
    "formaAcionamento",
    ]

    df = df.drop(columns=colunas_drop, errors="ignore")

    return df
