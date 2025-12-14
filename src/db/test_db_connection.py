import pandas as pd
from src.db.connection import get_engine

engine = get_engine()

df = pd.read_sql(
    "SELECT COUNT(*) AS total FROM ocorrencias",
    engine
)

print(df)