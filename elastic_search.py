from elasticsearch import Elasticsearch, helpers
import pandas as pd

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

df = pd.read_csv('./assets/data_final_w_sentiments.csv')

actions = [
    {
        "_index": "movies",
        "_id": row["uuid"], 
        "_source": {
            "movie_name": row["movie_name"],
            "movie_date": row["movie_date"],
            "movie_rating": row["movie_rating"],
            "movie_genre": row["movie_genre"],
            "comment_user": row["comment_user"],
            "comment_date": row["comment_date"],
            "comment_text": row["comment_text"],
            "result":row["result"]
        }
    }
    for index, row in df.iterrows()
]

helpers.bulk(es, actions)

print("Dados carregados com sucesso para o Elasticsearch")
