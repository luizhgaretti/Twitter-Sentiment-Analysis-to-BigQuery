# import Libs
import requests
from requests_oauthlib import OAuth1
from google.cloud import bigquery
from transformers import pipeline
import json
from transformers import pipeline

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

API_KEY = "coloque a key"
API_KEY_SECRET = "coloque a key"
ACCESS_TOKEN = "3coloque a key"
ACCESS_TOKEN_SECRET = "coloque a key"

auth = OAuth1(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

PROJECT_ID = "seu projeto no GCP"
DATASET_ID = "nome do dataset"
TABLE_ID = "nome da tabela"

sentiment_analyzer = pipeline("sentiment-analysis")

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        print(f"Erro ao buscar ID do usuário: {response.status_code}, {response.text}")
        return None

def get_user_tweets(user_id, max_results=10):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {"max_results": max_results}
    response = requests.get(url, auth=auth, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erro ao buscar tweets: {response.status_code}, {response.text}")
        return []

def insert_into_bigquery(rows):
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    errors = client.insert_rows_json(table_id, rows)
    if errors == []:
        print("Dados inseridos com sucesso no BigQuery.")
    else:
        print(f"Erros ao inserir no BigQuery: {errors}")

# Função principal
def process_user_tweets(username, max_results=10):
    user_id = get_user_id(username)
    if not user_id:
        print("ID do usuário não encontrado.")
        return

    print(f"ID do usuário '{username}': {user_id}")
    tweets = get_user_tweets(user_id, max_results=max_results)

    if not tweets:
        print("Nenhum tweet encontrado.")
        return

    rows_to_insert = []
    for tweet in tweets:
        text = tweet["text"]
        sentiment = sentiment_analyzer(text[:512])  # Limite de caracteres do modelo
        sentiment_label = sentiment[0]["label"]
        sentiment_score = sentiment[0]["score"]

        print(f"Tweet: {text}")
        print(f"Sentimento: {sentiment_label}, Score: {sentiment_score}")

        rows_to_insert.append({
            "tweet_id": tweet["id"],
            "username": username,
            "text": text,
            "sentiment": sentiment_label,
            "score": sentiment_score
        })

    insert_into_bigquery(rows_to_insert)

# Teste
if __name__ == "__main__":
    process_user_tweets("NOME DO USUARIO QUE QUER PEGAR O TWEET", max_results=10)
