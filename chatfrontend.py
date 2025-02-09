import streamlit as st
import chatbackend as glib  # Importa as funções do backend
from settings import DOMAIN_DESCRIPTIONS  # Importa as funções do backend

# Configurações da página
st.set_page_config(page_title="POC AI AGENT")
st.title("POC AI AGENT")

# Inicializa a memória e o histórico de chat, se ainda não existirem
if 'memory' not in st.session_state:
    st.session_state.memory = glib.create_memory()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'last_query' not in st.session_state:
    st.session_state.last_query = None  # Variável para rastrear se uma query SQL já foi gerada

# Renderiza o histórico de chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Caixa de entrada para o usuário
input_text = st.chat_input("Converse com o seu bot aqui")

if input_text:
    with st.chat_message("user"):
        st.markdown(input_text)
    st.session_state.chat_history.append({"role": "user", "text": input_text})

    if st.session_state.last_query is None:  # Gera uma query SQL se nenhuma tiver sido gerada ainda
        sql_query = glib.get_sql_from_question_bedrock(input_text, DOMAIN_DESCRIPTIONS, st.session_state.memory)
        st.write(sql_query)
        st.session_state.last_query = sql_query
        with st.chat_message("assistant"):
            st.markdown(f"Consulta SQL Gerada:\n```sql\n{sql_query}\n```")
        st.session_state.chat_history.append({"role": "assistant", "text": sql_query})

        returned_values = glib.query_postgresql(sql_query)
        st.write(returned_values)

        results, headers = glib.query_postgresql(sql_query)

        if isinstance(results, str) and results.startswith("Erro"):
            st.error(results)
        else:
            st.subheader("Resultados da Consulta")
            st.table(results)

            # Interpreta os resultados
            interpretation = glib.interpret_results_with_bedrock(input_text, results, headers, st.session_state.memory)
            with st.chat_message("assistant"):
                st.markdown(interpretation)
            st.session_state.chat_history.append({"role": "assistant", "text": interpretation})
    else:
        # Se já existe uma query, apenas continue a conversa com o contexto existente
        chat_response = glib.get_chat_response(input_text=input_text, memory=st.session_state.memory)
        with st.chat_message("assistant"):
            st.markdown(chat_response)
        st.session_state.chat_history.append({"role": "assistant", "text": chat_response})
        