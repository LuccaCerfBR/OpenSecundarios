# app.py

import streamlit as st
from sqlalchemy import create_engine, text

# Configuração do banco de dados MySQL
username = "root"
password = "Fksowo5AdObq3pM9vGO9"
host = "containers-us-west-89.railway.app"
port = "7254"
database = "railway"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Função para buscar todos os investimentos
def fetch_all_investments():
    query = "SELECT * FROM tb_investimentos"
    with engine.connect() as conn:
        return conn.execute(text(query)).fetchall()

# Função para contar o número de registros na tabela tb_investimentos
def count_investments():
    query = "SELECT COUNT(*) FROM tb_investimentos"
    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()

# Interface Streamlit
st.title("Streamlit com MySQL")

# Sidebar com opções de páginas
option = st.sidebar.selectbox(
    "Escolha uma página",
    ["SecundariosRF", "Fluxo RF dia", "Risco Retorno RF", "Curva FTP"]
)

# Exibir conteúdo com base na opção selecionada
if option == "SecundariosRF":
    # Check for changes in number of rows
    current_count = count_investments()
    last_count = st.session_state.get("last_count", None)

    if last_count is None:
        st.session_state["last_count"] = current_count
    elif last_count != current_count:
        st.session_state["last_count"] = current_count
        st.experimental_rerun()

    # Mostrar todos os dados da tb_investimentos
    st.write("Dados da tb_investimentos:")
    data = fetch_all_investments()
    if data:
        st.table(data)
    else:
        st.write("Nenhum dado encontrado na tabela tb_investimentos.")
elif option == "Fluxo RF dia":
    st.write("Conteúdo da página 'Fluxo RF dia'")
elif option == "Risco Retorno RF":
    st.write("Conteúdo da página 'Risco Retorno RF'")
elif option == "Curva FTP":
    st.write("Conteúdo da página 'Curva FTP'")
