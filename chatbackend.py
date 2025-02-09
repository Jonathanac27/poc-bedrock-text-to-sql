import boto3
import psycopg2
import json
import re
import os
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import BedrockChat
from langchain.prompts import PromptTemplate
from tabulate import tabulate
from dotenv import load_dotenv
from settings import DOMAIN_DESCRIPTIONS

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_llm():
    llm = BedrockChat(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", #set the foundation model
        model_kwargs= {                         
            "temperature": 0,
            "max_tokens": 1000,
            # "topP": 0.5, # Removido Depreciated
            # "maxTokenCount": 100, # Removido Depreciated
        }
    )
    return llm

# Configurar cliente AWS Bedrock
bedrock_client = boto3.client(
    'bedrock-runtime',  
    region_name='us-east-1'
)

# Function to configure the LLM with AWS Bedrock using the custom class

# Função para invocar o modelo Bedrock
def invoke_bedrock_model(prompt, model_id='anthropic.claude-3-5-sonnet-20240620-v1:0'):
    response = bedrock_client.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',  
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",  
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )
    
    return json.loads(response['body'].read().decode('utf-8'))

# Função para conectar ao PostgreSQL e executar uma consulta
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
    
# Função para transformar a pergunta em linguagem natural em uma consulta SQL usando Bedrock
def get_sql_from_question_bedrock(question, all_domain_descriptions, memory):
    prompt = (
        "Você é um assistente que transforma perguntas em linguagem natural em consultas SQL.\n"
        f"Sua tarefa é transformar a seguinte pergunta em uma consulta SQL: {question}. Considere que os dados vão estar em formato STRING"
        "Use os seguintes domínios de dados para auxiliar na criação da consulta SQL.\n"
        "Por favor, retorne apenas a consulta SQL dentro de um bloco ```sql```. Não inclua nenhuma outra explicação ou comentário."

    )
    
    # Adicionar descrições de colunas para todos os domínios
    for domain, details in all_domain_descriptions.items():
        schema_table = f"Schema: {details['schema']}, Tabela: {details['table']}"
        columns_description = "\n".join([f"{col}: {desc}" for col, desc in details["columns"].items()])
        prompt += f"\nDomínio {domain}:\n{schema_table}\n{columns_description}\n"
    
    # Invocar o modelo Bedrock para gerar a consulta SQL
    sql_response = invoke_bedrock_model(prompt)
    # sql_response = response.choices[0].message.content.strip() /// PONTO DE ATENÇÃO - VERIFICAR OUTPUT DO MODELO
    content = sql_response['content'][0]['text']  # Assuming it's always in the first item of content list

    # Usar regex para extrair a consulta SQL dentro do bloco ```sql```
    match = re.search(r'```sql\n(.*?)\n```', content, re.DOTALL)
    if match:
        query = match.group(1).strip()
    else:
        query = content

    memory.save_context({"input": question}, {"output": query})
    return query
    
# Função para interpretar os resultados com Bedrock
def interpret_results_with_bedrock(question, results, headers, memory):
    # Formatar a tabela para facilitar a leitura pelo modelo Bedrock
    table = tabulate(results, headers=headers, tablefmt="grid")

    prompt = (
        "Você é um assistente inteligente. Abaixo está uma pergunta feita por um usuário, seguida de uma tabela de dados que foi retornada por uma consulta SQL. "
        "Sua tarefa é analisar esses dados e responder à pergunta do usuário de forma clara e direta, levando em consideração os cabeçalhos da tabela.\n\n"
        f"Pergunta: {question}\n\nTabela de Dados:\n{table}\n\n"
        "Interprete esses dados e responda à pergunta acima com base nos resultados fornecidos."
    )
    
    try:
        # Invocar o modelo Bedrock para interpretar os resultados
        interpretation = invoke_bedrock_model(prompt)

        content = interpretation['content'][0]['text']  # Assuming it's always in the first item of content list check the output of the model

        memory.save_context({"input": question}, {"output": content})

        return content
    except Exception as e:
        return f"Erro ao interpretar os resultados: {e}"

# Função para criar a memória da sessão
def create_memory():
    llm = get_llm()
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=10000)
    return memory

# Função para obter a resposta do chatbot com contexto de memória
def get_chat_response(input_text, memory):
    llm = get_llm()  # Utilize o LLM personalizado Bedrock

    # Tenta carregar o histórico da memória, se existir
    # memory_variables = memory.load_memory_variables({})
    # history = memory_variables.get("history", "")

    # # Define um prompt template com o histórico atual
    # prompt_template = PromptTemplate(
    #     input_variables=["history", "input"],  # Certifique-se de que esses nomes correspondem às chaves usadas
    #     template="The following is a conversation between an AI assistant and a user. The assistant is helpful, creative, clever, and very friendly.\n\n"
    #              f"History:\n{history}\n\nUser: {input}\nAssistant:"
    # )

    conversation_with_memory = ConversationChain(
        llm=llm,        
        memory=memory,
        verbose=True
    )

    # Gera a resposta do chatbot com o contexto atual

    chat_response = conversation_with_memory.invoke(input = input_text) #pass the user message and summary to the model
    
    return chat_response['response']

    # chat_response = conversation_with_memory.predict(input={"input": input_text, "history": history})
    # return chat_response