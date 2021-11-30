
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

from services.InstagramGetData import getApiData, getUsername


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

def check_if_is_fake(account_data):
    dataToTree = pd.read_csv('user_fake_authentic_4class.csv')
    dataToTree['class'] = dataToTree['class'].replace(['r', 'a', 'i', 's'], [0, 1, 2, 3])

    # Dropar colunas cs e pi
    dataToTree = dataToTree.drop(['cs', 'pi'], axis=1)


    x = dataToTree.drop("class", axis=1)
    y = dataToTree["class"]

    Xtrain, Xval, Ytrain, Yval = train_test_split(x, y, test_size=0.5, random_state=0)

    trees = RandomForestClassifier(n_estimators=1000,random_state=None , n_jobs=-1)
    trees.fit(Xtrain, Ytrain)

    # Acurácia
    p = trees.score(Xval, Yval)

    lista = np.array(account_data)
    result = trees.predict(lista.reshape(1, -1))

    resultados_dict = {0: 'Real', 1: 'Fake', 2: 'Fake Inativo', 3: 'Possível SPAM'}
    
    return p*100, resultados_dict[result[0]]
    


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


json_file = st.file_uploader("Carregar o arquivo JSON da conta do Instagram", type=None, accept_multiple_files=False, on_change=None, args=None, kwargs=None)
st.text('Não sabe como obter o arquivo? Clique no botão que está no fim dessa página')

if json_file is not None:
    Result = None
    with st.spinner("Aguarde, estamos analisando a conta..."):
        data = getApiData(json_file)
        result = check_if_is_fake(data)

    username = getUsername(json_file)
    if result[1] == 'Fake' or result[1] == 'Fake Inativo':
        st.error(f"A conta **@{username}** foi classificada pelo algorítmo como **{result[1]}** com uma acurácia de **{result[0]:.2f}%**")
    elif result[1] == 'Real':
        st.success(f"A conta **@{username}** foi classificada pelo algorítmo como **{result[1]}** com uma acurácia de **{result[0]:.2f}%**")
    else:
        st.warning(f"A conta **@{username}** foi classificada pelo algorítmo como **{result[1]}** com uma acurácia de **{result[0]:.2f}%**")


show_instructions = st.checkbox('Clique aqui para obter as instruções de como obter o arquivo JSON')

if show_instructions:
    st.markdown("""
    Como o Instagram não disponibiliza uma API pública para usar o classificador você deve baixar um arquivo JSON contendo os dados contendo as informações sobre a conta.

    

### Passos:

1. Acesse [https://www.instagram.com/accounts/login/](https://www.instagram.com/accounts/login/) e faça **login** na sua conta;
2. Escolha qual usuário deseja analisar. Exemplo @instagram_user
3. Acesse [https://www.instagram.com/instagram_user/?__a=1](https://www.instagram.com/andrefbrito_/?__a=1) substituindo **instagram_user** pelo usuário que deseja consultar. **SEM o @.**
4. Quando a página carregar aperte `ctrl + s` ou clique em "salvar" no navegador. 
5. Salve o arquivo com a extensão `.json` no seu computador e carregue-o acima.

### ATENÇÃO:

**Não tente automatizar este processo usando bots ou autoclicks em páginas, por exemplo. Isso viola diretamente as diretrizes do Instagram e sua conta pode ser banida permanentemente por isso.**
""")
