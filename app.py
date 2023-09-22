# app.py

import streamlit as st
import pandas as pd
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
    query = "select * from vw_equities_data_financials"    
    
    with engine.connect() as conn:
        return conn.execute(text(query)).fetchall()




# Função para contar o número de registros na tabela tb_investimentos
def count_investments():
    query = "SELECT COUNT(*) FROM equities_data"
    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()

def custom_order(series):
    series_str = series.astype(str)
    split_series = series_str.str.split('.', expand=True).fillna(0).astype(int)
    return split_series.apply(tuple, axis=1)


# -------------- SETTINGS --------------

page_title = "XPTO AI"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


st.title(page_title + " " + page_icon)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Função para buscar todas as empresas
def fetch_all_companies():
    query = "SELECT DISTINCT DENOM_CIA FROM equities_data ORDER BY DENOM_CIA"
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(text(query)).fetchall()]

# Função para buscar todas as contas para uma empresa específica
def fetch_all_accounts_for_company(company):
    query = f"SELECT DISTINCT DS_CONTA FROM equities_data WHERE DENOM_CIA = '{company}' ORDER BY DS_CONTA"
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(text(query)).fetchall()]


# Sidebar com opções de páginas
companies = fetch_all_companies()
selected_company = st.sidebar.selectbox("Escolha uma empresa", companies)



# Sidebar com opções de páginas
option = st.sidebar.selectbox(
    "Escolha uma página",
    ["Financeiro", "Ratios", "Segments & KPIs"]
)




# Exibir conteúdo com base na opção selecionada
if option == "Financeiro":
    # Check for changes in number of rows
    current_count = count_investments()
    last_count = st.session_state.get("last_count", None)

    if last_count is None:
        st.session_state["last_count"] = current_count
    elif last_count != current_count:
        st.session_state["last_count"] = current_count
        st.experimental_rerun()

    # Mostrar todos os dados da tb_investimentos
    st.write("DF Individual - Demonstração do Resultado")
    data = fetch_all_investments()
    if data:
       # Convert data to DataFrame
        df = pd.DataFrame(data, columns=["DENOM_CIA", "DT_FIM_EXERC", "DS_CONTA", "VL_CONTA","ID"])
        
        # Divida os valores por 1000
        df["VL_CONTA"] = df["VL_CONTA"] / 1000
        
        # Selecione a empresa
        df = df[df["DENOM_CIA"] == selected_company]
        
        # Convert the 'DT_FIM_EXERC' column to datetime format
        df['DT_FIM_EXERC'] = pd.to_datetime(df['DT_FIM_EXERC'])
        
        # Format the 'DT_FIM_EXERC' column
        df['DT_FIM_EXERC'] = df['DT_FIM_EXERC'].dt.strftime("%b %y'")
        
        # Antes do agrupamento, crie o dicionário de ordem
        order_dict = df.drop_duplicates('DS_CONTA').set_index('DS_CONTA')['ID'].to_dict()
        
        # Prossiga com o agrupamento e criação da pivot table
        df = df.groupby(["DS_CONTA", "DT_FIM_EXERC"]).sum()["VL_CONTA"].reset_index()
        pivot_df = df.pivot(index="DS_CONTA", columns="DT_FIM_EXERC", values="VL_CONTA")
        
        # Ordene a pivot_df usando o dicionário de ordem
        pivot_df = pivot_df.loc[pivot_df.index.to_series().map(order_dict).sort_values().index]
        
        # Formate os números na pivot_df
        pivot_df = pivot_df.applymap(lambda x: f"R$ {x:,.2f}")

        # Remova os caracteres 'R$' e as vírgulas da pivot_df e converta para float
        pivot_df = pivot_df.replace('[R$,]', '', regex=True).astype(float)
        
        # Preencha os valores NaN com zero
        pivot_df = pivot_df.fillna(0)
        
        # Arredonde os valores na pivot_df
        pivot_df = pivot_df.round(0).astype(int)
        
        # Formate os números na pivot_df
        pivot_df = pivot_df.applymap(lambda x: f"R$ {x:,.0f}")
        
        # Mostre a tabela com números alinhados à direita
        st.write(pivot_df.style.set_properties(**{'text-align': 'right'}))

        # Permita que o usuário selecione DS_CONTA da lista
        selected_account = st.selectbox("Selecione uma conta:", list(pivot_df.index))


        
        # Filtrar os dados com base na conta selecionada e plotar
        filtered_data = df[df["DS_CONTA"] == selected_account]
        st.bar_chart(filtered_data.set_index("DT_FIM_EXERC")["VL_CONTA"].rename("R$ (milhares)"))
                            
                    
    else:
        st.write("Nenhum dado encontrado na tabela tb_investimentos.")
elif option == "Analises":
    st.write("Conteúdo da página 'Fluxo RF dia'")
elif option == "Financeiro":
    st.write("Conteúdo da página 'Risco Retorno RF'")
elif option == "Ratios":
    st.write("Conteúdo da página 'Curva FTP'")