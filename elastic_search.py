import csv
from elasticsearch import Elasticsearch, helpers
import pandas as pd

# Conectar ao Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Ler o CSV usando pandas
df = pd.read_csv('./assets/data.csv')

# Transformar os dados para o formato que o Elasticsearch espera
actions = [
    {
        "_index": "movies",
        "_id": row["uuid"],  # Usar o UUID como ID do documento
        "_source": {
            "movie_name": row["movie_name"],
            "movie_date": row["movie_date"],
            "movie_rating": row["movie_rating"],
            "movie_genre": row["movie_genre"],
            "comment_user": row["comment_user"],
            "comment_date": row["comment_date"],
            "comment_text": row["comment_text"]
        }
    }
    for index, row in df.iterrows()
]

# Carregar os dados para o Elasticsearch
helpers.bulk(es, actions)

print("Dados carregados com sucesso para o Elasticsearch")
