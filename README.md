# Twitter Sentiment Analysis to BigQuery
Este projeto busca tweets de um usuário no Twitter, realiza análise de sentimento em cada tweet usando o modelo distilbert-base-uncased-finetuned-sst-2-english da biblioteca transformers e armazena os resultados no Google BigQuery.

-----------------------------------

# Estrutura do Código / Funcionalidades
- Busca de tweets recentes de um usuário específico usando a API do Twitter.
- Realiza análise de sentimento em cada tweet (positivo, negativo, neutro). Para essa analise, utilizamos o modelo distilbert-base-uncased-finetuned-sst-2-english da biblioteca transformer
- Armazenar os tweets e os resultados da análise de sentimento em uma tabela do BigQuery.

obs: O Código não está com estratégia NRT, devido a limitação do plano free da API do Twitter Developer.

-----------------------------------

# Pré - Requesitos ⚠️
### Credenciais do Twitter/X
- Obtenha uma chave de API e token de acesso no site do twitter developer (https://developer.x.com/en)
- Se atente em criar o projeto e associar ao app, caso contrário, seu codigo receberá erro de autenticação
- Optei por utilizar a autenticação OAuth1, utilizando as chaves:
```
auth = OAuth1(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
```
- Gere as chaves via https://developer.x.com/en 

### Configuração do Google Cloud
- Crie uma Service Account, adicione as roles: xxx
- Gere a secret e baixe o JSON do credenciais.
- Coloque o credenciais.json no mesmo diretório do seu .py
- Configure a variável e ambiente para autenticação do GCP, utilizando a Service Account.
```
export GOOGLE_APPLICATION_CREDENTIALS="/path/credentials.json"
```
- Crie um dataset e uma tabela no BigQuery com o seguinte schema:
``` sql
  [
      {"tweet_id", "STRING"},
      {"username", "STRING"},
      {"text", "STRING"},
      {"sentiment", "STRING"},
      {"score", "FLOAT"},
      {"created_at", "TIMESTAMP"}
  ]
```

### Dependências Python
- Instale as bibliotecas necessárias:
```
pip install requests requests-oauthlib google-cloud-bigquery transformers
```
```
pip install tweepy google-cloud-pubsub google-cloud-bigquery
```

### Altere as Keys e informações do GCP
- Substitua API_KEY, API_KEY_SECRET, ACCESS_TOKEN, e ACCESS_TOKEN_SECRET pelas suas credenciais do Twitter.
```
API_KEY = "coloque sua api key aqui"
API_KEY_SECRET = "coloque sua api key secret aqui"
ACCESS_TOKEN = "coloque seu access token aqui"
ACCESS_TOKEN_SECRET = "coloque seu access token secret aqui"
```
- Atualize as variáveis PROJECT_ID, DATASET_ID e TABLE_ID com os valores do seu projeto no BigQuery.
```
PROJECT_ID = "id do projeto no GCP"
DATASET_ID = "nome do dataset"
TABLE_ID = "nome da tabela"
```

-----------------------------------

# Uso
No seu terminal, execute
```
python seu_codigo.py
```
O script buscará os tweets, analisará os sentimentos e armazenará os dados no BigQuery.

Exemplo de Saída no Terminal

```
ID do usuário 'usuario': 123456789
Tweet: texto do tweet 01.
Sentimento: POSITIVE, Score: 0.98
Tweet: texto do tweet 01.
Sentimento: POSITIVE, Score: 0.87
Dados inseridos com sucesso no BigQuery.
```

obs: Se receber o erro abaixo, possivelmente sua account billing no GCP não está ativa. No modelo free, a API do Big Query não permite ingestão "NRT", se não quiser habilitar o billing, você tem como saída gerar um JSON com os tweets e depois realizar a ingestão via batch no Big Query
```
google.api_core.exceptions.Forbidden: 403 POST https://bigquery.googleapis.com/bigquery/v2/projects/garetti/datasets/twitter/tables/tweets2/insertAll?prettyPrint=false: Access Denied: BigQuery BigQuery: Streaming insert is not allowed in the free tier
```
Exemplo de código extraindo JSON (Não fiz o teste para validar 100%, o código pode conter algum erro de lógica)
```
import json
from google.cloud import bigquery

def save_to_file(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)
save_to_file(rows_to_insert, "tweets.json")

def load_file_to_bigquery(file_path, table_id):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )
    with open(file_path, "rb") as file:
        job = client.load_table_from_file(file, table_id, job_config=job_config)
    job.result() 
load_file_to_bigquery("tweets.json", "seu-codigo")
```

-----------------------------------

# Clone este repositório:
git clone https://github.com/seu-usuario/twitter-sentiment-bq.git
cd twitter-sentiment-bq

-----------------------------------

# Contribuições
- Contribuições são bem-vindas ;)
- Se tiver interesse, faça o Fork do repo.
- Crie uma branch:
```
git checkout -b ajuste-codigo
```
- Envie suas alterações:
```
git push origin ajuste-codigo
```
- Manda um Pull Request que analiso e aceito a alterção no código original ;) 

