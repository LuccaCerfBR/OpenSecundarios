# app.py

import streamlit as st
from sqlalchemy import create_engine, text

# Configuração do banco de dados SQL Server
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=localhost\SQLEXPRESS;'
    r'DATABASE=master;'  # Substitua 'YourDatabaseName' pelo nome do seu banco de dados
    r'Trusted_Connection=yes;'  # Isso usa autenticação do Windows
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

# connection_string = "mssql+pyodbc://usrbancsec:perigo@localhost:8501/master?driver=ODBC+Driver+17+for+SQL+Server"
# engine = create_engine(connection_string)


# Função para buscar todos os tenores disponíveis
def fetch_tenors():
    query = "SELECT DISTINCT tenor FROM XP_INVEST_RF_BANC_RELATIVE"
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(text(query)).fetchall()]

# Função para buscar dados da query especificada com filtro por tenor
def fetch_custom_data(tenor=None):
    query = "SELECT * FROM XP_INVEST_RF_BANC_RELATIVE where dataref= '2023-09-04'"
    if tenor:
        query += f" AND tenor = '{tenor}'"
    with engine.connect() as conn:
        return conn.execute(text(query)).fetchall()

# Interface Streamlit
st.title("Streamlit com SQL Server")

# Widget de seleção de tenor
available_tenors = fetch_tenors()
selected_tenor = st.selectbox("Selecione o Tenor", ["Todos"] + available_tenors)

# Mostrar dados da query com filtro por tenor
st.write("Dados da query:")
data = fetch_custom_data(tenor=None if selected_tenor == "Todos" else selected_tenor)
if data:
    st.table(data)
else:
    st.write("Nenhum dado encontrado para a data de referência '2023-09-04' com o tenor selecionado.")
