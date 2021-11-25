
import streamlit as st
import pandas as pd
import plotly.express as px

from services.InstagramGetData import getApiData


st.set_page_config(layout="wide")

DATA_URL = "https://raw.githubusercontent.com/ArthurCisotto/P2_CDados/main/user_fake_authentic_4class.csv"

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)

    return data

data = load_data(10000)

def generate_correlation_chart(df):
    x=df.corr()
    lista = x.values.tolist()
    fig = px.imshow(lista,  labels=dict(x="Features", y="Features", color="Correlação"),
                x=['pos', 'flw', 'flg', 'bl', 'pic', 'lin', 'cl', 'cz', 'ni', 'erl', 'erc', 'lt', 'hc', 'pr', 'fo', 'cs', 'pi'],
                y=['pos', 'flw', 'flg', 'bl', 'pic', 'lin', 'cl', 'cz', 'ni', 'erl', 'erc', 'lt', 'hc', 'pr', 'fo', 'cs', 'pi'],
                zmax = 1, zmin = -1)
    st.plotly_chart(fig, use_container_width=True)


# Header
row1_1, row1_2 = st.columns(2)

with row1_1:
    st.title("Projeto 2 Cdados")
    st.write("Com 💗 por **Alessandra Ogawa, André Brito, Arthur Cisotto, Camila Bernardi**")

with row1_2:
    st.write("""
    ###
    O projeto tem como objetivo prever se um usuário do Instagram é fake ou não a partir de
    dados da conta daquele usuário
    """)

st.title("Gráfico de correlação")
generate_correlation_chart(data)


json_file = st.file_uploader("Carregar o arquivo de conta JSON", type=None, accept_multiple_files=False, on_change=None, args=None, kwargs=None)
if json_file is not None:
    data = getApiData(json_file)
    print(data)
# # Inputs

# row3_1, row3_2, row3_3 = st.columns(3)
# with row3_1:
#   choice = st.number_input("Pick", step=1)