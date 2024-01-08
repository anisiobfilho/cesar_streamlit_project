import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
     page_title="Resultados de Natação em Tóquio 2020",
     page_icon="🏊‍♂️",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={}
 )

st.cache_resource.clear()

## MAIN
st.header("Análise Exploratória")

@st.cache_resource
def carrega_base(path):
    data = pd.read_csv(path, sep=",", low_memory=True)
    return data

data_dict = pd.DataFrame()

data_dict['Variáveis'] = ['place', 'heat', 'lane', 'name', 'country', 'reaction time', 'dq', 'event', 'splits', 'relay_swimmer', 'relay_swimmer_X_gender']
data_dict['Definição'] = [
    "Ordem de finalização por bateria",
    "There are three types of heats, which are 'heat', 'semi', and 'final'. Each race has multiple heats, denoted as 'heat_1', 'heat_2' etc. Some races have semis, again as 'semi_1', 'semi_2'. All races have only one final, called just 'final'. Athletes placing well enough in the heats advance to the semis (if held) and athletes placing high enough in the semis (or heats if there are no semis) advance to the final.",
    "Existem 8 raias, 1-8",
    "Nome do atleta como SOBRENOME Nome. Existem algumas exceções para atletas com vários nomes/sobrenomes ou letras maiúsculas não padrão em qualquer um dos nomes, por ex. 'McKEON Emma' para Emma McKeon. O valor será NA para revezamentos, consulte as colunas relay_swimmer.",
    "Código do país de três letras.",
    "O tempo decorrido entre o sinal de partida e a saída do atleta do bloco de partida, em segundos.",
    "Um atleta foi desclassificado? Se 0, então não, a corrida foi disputada legalmente. Se 1 então sim, o atleta foi desclassificado por alguma infração de regra.",
    "Nome do evento. String contendo gênero (masculino, feminino, misto), distância (em metros) e discípulo (nado livre, costas etc.).",
    "Apresentado como split_50, split_100 etc. As divisões NÃO são cumulativas. Em vez disso, eles são aditivos. Portanto, o valor split_50 é o tempo, em segundos, que um atleta percorre os primeiros 50 metros. Então split_100 é o tempo, em segundos, para o atleta percorrer os próximos 50 metros. Isso significa que no momento do atleta percorrer 100 metros é split_50 + split_100. Para eventos menores que uma determinada divisão, o valor split_X será NA.",
    "Apresentado como relay_swimmer_1 etc. O nome de cada nadador em um revezamento por ordem de competição. Cada revezamento conta com quatro nadadores. São usadas convenções de nomenclatura da coluna de nome.",
    "Gênero do nadador de revezamento por posição para uso em provas de revezamento misto. Ou 'f' para mulher ou 'm' para homem. Se o evento não for um revezamento misto esse valor será NA.",
]
st.subheader("Dicionário de Dados")
st.dataframe(data_dict, use_container_width=True)

st.subheader("Base de dados")
df = carrega_base("data/tokyo_2020_swim.csv")
st.dataframe(df, use_container_width=True)



