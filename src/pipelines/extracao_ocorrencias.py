import pandas as pd
from sqlalchemy import text
from src.db.connection import get_engine

def extract_ocorrencias(limit: int | None = None) -> pd.DataFrame:
    """
    Extrai dados básicos de ocorrências para análise e ML
    """
    engine = get_engine()

    query = """
        SELECT
            o.id,
            o.dataHoraChamada,
            o.statusAtendimento,
            o.formaAcionamento,
            o.naturezaOcorrenciaId,
            o.grupoOcorrenciaId,
            o.subgrupoOcorrenciaId,
            o.unidadeOperacionalId,
            l.municipio
        FROM ocorrencias o
        JOIN localizacoes l ON l.id = o.localizacaoId
        WHERE o.dataHoraChamada IS NOT NULL
    """

    if limit:
        query += f" LIMIT {limit}"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return df