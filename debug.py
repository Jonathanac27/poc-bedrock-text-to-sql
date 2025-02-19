# DEBUGGING SEGMENT //

import boto3
import json
from settings import DOMAIN_DESCRIPTIONS
import re
import os
import psycopg2

ACESS_KEY = os.getenv('ACESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
# Criação do cliente Bedrock Runtime
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1', aws_access_key_id=ACESS_KEY, aws_secret_access_key=SECRET_KEY)

# Função para obter o LLM e invocar o modelo

def query_postgresql(query):
    try:
        connection = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password")
        )
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        cursor.close()
        connection.close()
        
        return records, column_names

    except (Exception, psycopg2.Error) as error:
        return f"Erro ao conectar ao PostgreSQL: {error}"
    
def get_llm(input_text):
    # Monta o payload no formato correto
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": input_text
            }
        ]
    }
    # Converte o payload em JSON e depois para bytes
    payload_bytes = json.dumps(payload).encode('utf-8')

    # Faz a chamada ao modelo através do Bedrock
    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        contentType="application/json",
        accept="application/json",
        body=payload_bytes
    )

    # Retorna a resposta do modelo
    return json.loads(response['body'].read().decode('utf-8'))

question = '''
Quantos clientes fizeram investiram no google em 2024?
'''    

prompt = (
        "Você é um assistente especializado em transformar perguntas em consultas SQL.\n"
        f"Sua tarefa é transformar a seguinte pergunta em uma consulta SQL: {question}\n\n"
        "IMPORTANTE:\n"
        "- Todos os campos no banco de dados estão armazenados como VARCHAR/STRING\n"
        "- Para operações matemáticas, use CAST(campo AS TIPO), exemplo:\n"
        "  * Para números inteiros: CAST(valor AS INTEGER)\n"
        "  * Para decimais: CAST(valor AS DECIMAL(10,2))\n"
        "  * Para datas: CAST(data AS DATE)\n"
        "- Sempre use CAST ao comparar ou calcular valores numéricos\n\n"
        "Use os seguintes domínios de dados para auxiliar na criação da consulta SQL:\n"
        "Por favor, retorne apenas a consulta SQL dentro de um bloco ```sql```. Não inclua nenhuma outra explicação ou comentário."
        )

for domain, details in DOMAIN_DESCRIPTIONS.items():
        schema_table = f"Schema: {details['schema']}, Tabela: {details['table']}"
        columns_description = "\n".join([f"{col}: {desc}" for col, desc in details["columns"].items()])
        prompt += f"\nDomínio {domain}:\n{schema_table}\n{columns_description}\n"

response = get_llm(prompt)

# Invocar o modelo Bedrock para gerar a consulta SQL
sql_response = response
# sql_response = response.choices[0].message.content.strip() /// PONTO DE ATENÇÃO
content = sql_response['content'][0]['text']  # Assuming it's always in the first item of content list

# Usar regex para extrair a consulta SQL dentro do bloco ```sql```
match = re.search(r'```sql\n(.*?)\n```', content, re.DOTALL)
if match:
    query = match.group(1).strip()
else:
    query = content

query_postgresql(query)

print(response)