import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Carregar as variáveis de ambiente
load_dotenv()

# Função para criar o catálogo a partir do CSV
def generate_catalog_from_csv(schema, table_name, csv_file, output_file):
    # Carregar o CSV em um DataFrame
    df = pd.read_csv(csv_file)
    
    # Gerar as colunas com descrições vazias
    columns = {col: "" for col in df.columns}
    
    # Estruturar o catálogo no formato solicitado
    catalog = {
        schema: {
            "schema": schema,
            "table": table_name,
            "columns": columns
        }
    }
    
    # Salvar o catálogo em um arquivo Python
    with open(output_file, 'w') as file:
        file.write("DOMAIN_DESCRIPTIONS = {\n")
        file.write(f'    "{schema}": {{\n')
        file.write(f'        "schema": "{schema}",\n')
        file.write(f'        "table": "{table_name}",\n')
        file.write(f'        "columns": {{\n')
        
        for col, desc in columns.items():
            file.write(f'            "{col}": "{desc}",\n')
        
        file.write("        }\n")
        file.write("    }\n")
        file.write("}\n")

    print(f"Catálogo gerado com sucesso e salvo em {output_file}")

# Função de conexão com o banco de dados SQL Server
def get_db_engine():
    user = os.getenv("user_sql")
    password = os.getenv("password_sql")
    host = os.getenv("host_sql")
    port = os.getenv("port_sql")
    dbname = os.getenv("database_sql")
    
    # Montar a string de conexão para SQL Server
    db_url = f"mssql+pyodbc://{user}:{password}@{host}:{port}/{dbname}?driver=ODBC+Driver+17+for+SQL+Server"
    
    # Criar o engine
    return create_engine(db_url)

# Função para criar a tabela automaticamente com base no schema
def create_table_from_csv(engine, schema, table_name, csv_file):
    # Carregar o CSV em um DataFrame
    df = pd.read_csv(csv_file)
    
    # Definir o metadata
    metadata = MetaData(schema=schema)
    
    # Definir as colunas automaticamente com base no DataFrame
    columns = [Column(col, String) for col in df.columns]
    
    # Criar a tabela no banco de dados
    table = Table(table_name, metadata, *columns, extend_existing=True)
    metadata.create_all(engine)

# Função para inserir os dados do CSV na tabela
def load_csv_to_db(engine, schema, table_name, csv_file):
    # Criar o DataFrame a partir do CSV
    df = pd.read_csv(csv_file)
    inserted_at = 'inserted_at'
    df = df.astype('string')
    df[f'{inserted_at}'] = datetime.now()

    # Enviar os dados para o banco de dados
    df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)


if __name__ == "__main__":
    # Definir variáveis
    schema = 'schema_alvo'  # Altere para o schema desejado
    table_name = 'tabela_alvo'  # Altere para o nome da tabela desejada
    csv_folder = 'files-to-sql'  # Pasta onde os arquivos CSV estão localizados
    NOME_DO_CSV = 'csv_alvo.csv'  # Nome do arquivo CSV
    csv_file = os.path.join(csv_folder, NOME_DO_CSV)  # Caminho completo para o arquivo CSV
    output_file = 'catalogo_gerado.py'  # Nome do arquivo de saída

    # Criar a conexão com o banco de dados SQL Server
    engine = get_db_engine()
    
    # Criar a tabela automaticamente
    create_table_from_csv(engine, schema, table_name, csv_file)
    
    # Carregar os dados do CSV para o banco de dados
    load_csv_to_db(engine, schema, table_name, csv_file)

    # Gerar o catálogo
    generate_catalog_from_csv(schema, table_name, csv_file, output_file)
    
    print("Dados carregados com sucesso!")
