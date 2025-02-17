import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker

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

# Função de conexão com o banco de dados
def get_db_engine():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    dbname = os.getenv("database")
    
    # Montar a string de conexão
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
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
    
    # Enviar os dados para o banco de dados
    df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)

if __name__ == "__main__":
    # Definir variáveis
    schema = 'public'  # Altere para o schema desejado
    table_name = 'cdp_ef'  # Altere para o nome da tabela desejada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder = os.path.join(current_dir, 'files_to_db')
    NOME_DO_CSV = 'mock_data.csv'  # Nome do arquivo CSV
    csv_file = os.path.join(csv_folder, NOME_DO_CSV)
    output_file = 'catalogo_gerado.py'  # Nome do arquivo de saída
    
    # Criar a conexão com o banco de dados
    engine = get_db_engine()
    
    # Criar a tabela automaticamente
    create_table_from_csv(engine, schema, table_name, csv_file)
    
    # Carregar os dados do CSV para o banco de dados
    load_csv_to_db(engine, schema, table_name, csv_file)

    # Gerar o catálogo
    generate_catalog_from_csv(schema, table_name, csv_file, output_file)
    
    print("Dados carregados com sucesso!")
