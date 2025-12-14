from src.pipelines.extracao_ocorrencias import extract_ocorrencias

if __name__ == "__main__":
    df = extract_ocorrencias(limit=10)
    df.head()
    df.info()