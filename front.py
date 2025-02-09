import streamlit as st
import chatbackend as glib
from settings import DOMAIN_DESCRIPTIONS

# Configurações da página
st.set_page_config(
    page_title="POC AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 2.5rem !important;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .sql-query {
        background-color: #f1f3f5;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar com informações e configurações
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="POC AI Agent")
    st.header("Configurações")
    
    # Opções de configuração
    temperature = st.slider("Temperatura da IA", 0.0, 1.0, 0.7)
    show_sql = st.checkbox("Mostrar consultas SQL", value=True)
    
    # Botão para limpar histórico
    if st.button("Limpar Histórico"):
        st.session_state.chat_history = []
        st.session_state.memory = glib.create_memory()
        st.session_state.last_query = None
        st.experimental_rerun()

# Título principal com ícone
st.title("🤖 POC AI Agent")

# Inicialização do estado da sessão
if 'memory' not in st.session_state:
    st.session_state.memory = glib.create_memory()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = None

# Container principal do chat
chat_container = st.container()

# Área de chat com scroll
with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "sql" in message.get("type", ""):
                st.code(message["text"], language="sql")
            else:
                st.markdown(message["text"])

# Input do usuário
input_text = st.chat_input("Digite sua pergunta aqui...")

if input_text:
    # Mostra a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(input_text)
    st.session_state.chat_history.append({"role": "user", "text": input_text})

    # Processamento da primeira consulta
    if st.session_state.last_query is None:
        with st.spinner("Gerando consulta SQL..."):
            sql_query = glib.get_sql_from_question_bedrock(
                input_text, 
                DOMAIN_DESCRIPTIONS, 
                st.session_state.memory
            )
            
            if show_sql:
                with st.chat_message("assistant"):
                    st.markdown("**Consulta SQL Gerada:**")
                    st.code(sql_query, language="sql")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "text": sql_query,
                    "type": "sql"
                })

            st.session_state.last_query = sql_query

            # Execução da consulta
            with st.spinner("Executando consulta..."):
                results, headers = glib.query_postgresql(sql_query)

                if isinstance(results, str) and results.startswith("Erro"):
                    st.error(results)
                else:
                    # Exibe os resultados em uma tabela estilizada
                    st.markdown("### Resultados da Consulta")
                    st.dataframe(
                        results,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Interpretação dos resultados
                    with st.spinner("Interpretando resultados..."):
                        interpretation = glib.interpret_results_with_bedrock(
                            input_text,
                            results,
                            headers,
                            st.session_state.memory
                        )
                        with st.chat_message("assistant"):
                            st.markdown(interpretation)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "text": interpretation
                        })

    else:
        # Continuação da conversa
        with st.spinner("Processando..."):
            chat_response = glib.get_chat_response(
                input_text=input_text,
                memory=st.session_state.memory
            )
            with st.chat_message("assistant"):
                st.markdown(chat_response)
            st.session_state.chat_history.append({
                "role": "assistant",
                "text": chat_response
            })

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Desenvolvido com ❤️ por Jonathan A C"
    "</div>",
    unsafe_allow_html=True
)