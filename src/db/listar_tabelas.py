from sqlalchemy import text
from src.db.connection import get_engine

engine = get_engine()

with engine.connect() as conn:
    result = conn.execute(text("SHOW TABLES"))
    for row in result:
        print(row[0])
