# POC Bedrock Text-to-SQL

Este projeto implementa uma aplicação web usando [Streamlit](https://streamlit.io/) que integra a AWS Bedrock e Langchain para transformar perguntas em linguagem natural em consultas SQL, executar as consultas em um banco de dados PostgreSQL, e interpretar os resultados.

## Funcionalidades

1. **Transformação de Perguntas em SQL**: O aplicativo usa a integração com o AWS Bedrock (Claude) para gerar consultas SQL a partir de perguntas em linguagem natural.
2. **Execução de Consultas SQL**: As consultas geradas são executadas em um banco de dados PostgreSQL, e os resultados são exibidos diretamente na interface.
3. **Interpretação dos Resultados**: A aplicação também usa o AWS Bedrock para interpretar os resultados das consultas SQL e fornecer uma explicação detalhada dos dados.
4. **Memória de Conversação**: O chatbot mantém o histórico de interações utilizando o `ConversationSummaryBufferMemory` da Langchain, permitindo que o contexto das interações anteriores seja considerado nas conversas subsequentes.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter as seguintes dependências instaladas:

1. **Python 3.7 ou superior**: [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL**: Certifique-se de que você tem acesso a um banco de dados PostgreSQL.
3. **AWS CLI**: Configure suas credenciais AWS, pois o projeto utiliza o AWS Bedrock para processamento de linguagem natural. Para configurar o CLI, siga [este guia](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
4. **Dependências do Projeto**: Certifique-se de ter um arquivo `.env` com as variáveis de ambiente necessárias, como as credenciais do banco de dados e as configurações da AWS.

## Instalação

### 1. Clonar o Repositório

Clone o repositório para o seu ambiente local:
```bash
git clone https://github.com/SEU-USUARIO/poc-bedrock-text-to-sql.git


.
├── chatfrontend.py           # Interface de front-end usando Streamlit
├── chatbackend.py            # Lógica de back-end para gerar e interpretar queries
├── settings.py               # Configurações de domínio e outras definições
├── requirements.txt          # Lista de dependências do projeto
├── .env                      # Arquivo contendo as variáveis de ambiente
├── README.md                 # Documentação do projeto
└── .venv/                    # Ambiente virtual (criado automaticamente)
```cmd
cd poc-bedrock-text-to-sql
```cmd
python -m venv .venv

```cmd
source .venv/bin/activate

```cmd
.venv\Scripts\activate

```cmd
pip install -r requirements.txt

# Configurações do PostgreSQL
host=SEU_HOST_DO_POSTGRESQL
database=NOME_DO_SEU_BANCO_DE_DADOS
user=SEU_USUARIO_DO_BANCO
password=SUA_SENHA_DO_BANCO

# Credenciais da AWS
AWS_ACCESS_KEY_ID=SEU_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=SUA_SECRET_KEY
AWS_DEFAULT_REGION=SUA_REGIAO_AWS 

# Outras configurações, se necessário

streamlit run chatfrontend.py


### Alterações Adicionais:
- **Seção de Ambiente Virtual (venv)**: Expliquei como criar e ativar um ambiente virtual para isolar as dependências.
- **Seção `.env`**: Incluí mais detalhes sobre o arquivo `.env` e como configurá-lo.
- **Instruções Detalhadas para Instalação**: Agora detalha todos os passos desde clonar o repositório até rodar a aplicação com o ambiente virtual.

## Pré-requisitos

Certifique-se de ter o Python e as seguintes bibliotecas instaladas:

- pandas
- SQLAlchemy
- python-dotenv
- psycopg2-binary (para conexão com o PostgreSQL)

Para instalar as dependências, rode:

```bash
pip install pandas SQLAlchemy python-dotenv psycopg2-binary


**Detalhes Especificos da Aplicação**
A aplicação é composta por dois principais componentes:

Frontend: Implementado em chatfrontend.py usando Streamlit. Ele fornece a interface do usuário para interagir com o chatbot.
Backend: Implementado em chatbackend.py. Ele contém a lógica para transformar perguntas em consultas SQL, executar consultas no PostgreSQL e interpretar os resultados usando AWS Bedrock.
Detalhes do Langchain
Langchain é uma biblioteca que facilita a integração de modelos de linguagem com fluxos de trabalho de dados. Neste projeto, Langchain é usado para:

Memória de Conversação: Utiliza ConversationSummaryBufferMemory para manter o histórico de interações.
Cadeias de Conversação: Utiliza ConversationChain para gerenciar o fluxo de conversação entre o usuário e o chatbot.
Modelos de Linguagem: Integração com AWS Bedrock para gerar consultas SQL e interpretar resultados.
Para mais informações sobre Langchain, visite a documentação oficial.

### Ativação do Modelo de Marketing no AWS Bedrock
**Criar uma função IAM com permissões para Bedrock:**

Acesse o console do IAM na AWS.
Crie uma nova função com permissões para acessar o serviço Bedrock.
Anexe as políticas necessárias, como AmazonBedrockFullAccess.
Ativar o modelo de marketing:

No console do AWS Bedrock, navegue até a seção de modelos.
Selecione o modelo de marketing (por exemplo, anthropic.claude-3-5-sonnet-20240620-v1:0).
Siga as instruções para ativar o modelo na documentação da aws:
 https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html

![image](https://github.com/user-attachments/assets/234c351e-3412-4958-9e80-c56b1651b2f7)
