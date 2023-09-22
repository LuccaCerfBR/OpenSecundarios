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

# Interface Streamlit
st.title("Streamlit com MySQL")

# Mostrar todos os dados da tb_investimentos
st.write("Dados da tb_investimentos:")
data = fetch_all_investments()
if data:
    st.table(data)
else:
    st.write("Nenhum dado encontrado na tabela tb_investimentos.")
