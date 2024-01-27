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
st.sidebar.image("img/mascot.png")

st.cache_resource.clear()

## MAIN
st.header("Base de Dados")

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
st.dataframe(data_dict, hide_index=True, use_container_width=True)

st.subheader("Base de dados")
tokyo2020 = carrega_base("data/tokyo_2020_swim.csv")
st.dataframe(tokyo2020, use_container_width=True)

st.subheader("Limpeza e Pré-processamento de Dados")

st.write("As colunas 'place' e 'lane' representam a colocação do competidor (competidora ou equip) ao terminar a prova e a raia onde ele (eles) competiu. Portanto, seus tipos devem ser inteiros e não flutuantes. Também dropamos colunas linhas contendo valores NaN.")

st.write("Na coluna 'team', existem alguns valores diferentes que representam o mesmo país, como por exemplo 'USA' and 'USA - United States of America'. Então, substituímos e padronizamos.")

st.write("Ainda na coluna 'team' existiam dois valores numéricos ('0.65' e '0.66') que não representavam países e que foram excluídos")

st.write("Colunas que não serão necessarias para analise: Relay swimmer(todas), Relay swimmer gender (todas)")

st.write("As colunas de name e relay swimmer representam respectivamente nome dos nadadores e o nome dos nadadores que realizaram o revezamento. Já o relay swimmer gender representa o gênero do nadador que fez o revezamento")

st.write("Apenas atletas desqualificados não foram analisados. Logo utilizamos apenas os valores da coluna 'dq' == True.")

st.write("A base limpa e pré-processada ficou da seguinte forma:")

tokyo2020.dropna(subset=['place', 'lane'], inplace=True)
tokyo2020.loc[:, 'place'] = tokyo2020['place'].astype(int)
tokyo2020.loc[:, 'lane'] = tokyo2020['lane'].astype(int)
replace_dict = {'USA - United States of America': 'USA', 'ITA - Italy': 'ITA', 'AUS - Australia': 'AUS',
                'CAN - Canada':'CAN', 'HUN - Hungary': 'HUN', 'FRA - France':'FRA', 'ROC - ROC':'ROC', 'BRA - Brazil':'BRA', 'SRB - Serbia':'SRB',
                'POL - Poland':'POL', 'JPN - Japan':'JPN', 'GRE - Greece':'GRE', 'GBR - Great Britain':'GBR', 'NED - Netherlands':'NED',
                'SUI - Switzerland':'SUI', 'GER - Germany':'GER', "CHN - People's Republic of China":'CHN', 'BLR - Belarus':'BLR','ISR - Israel':'ISR',
                'KOR - Republic of Korea':'KOR', 'IRL - Ireland':'IRL','SWE - Sweden':'SWE', 'DEN - Denmark':'DEN', 'HKG - Hong Kong, China':'HKG','CZE - Czech Republic':'CZE',
                'RSA - South Africa':'RSA', 'ESP - Spain':'ESP','TUR - Turkey':'TUR', 'NZL - New Zealand':'NZL' }
tokyo2020.loc[:, 'team'] = tokyo2020['team'].replace(replace_dict)
tokyo2020 = tokyo2020[~tokyo2020['team'].isin(['0.65', '0.66'])].copy()
tokyo2020.drop(['relay_swimmer_1', 'relay_swimmer_2', 'relay_swimmer_3','relay_swimmer_4', 'relay_swimmer_1_gender', 'relay_swimmer_2_gender', 'relay_swimmer_3_gender', 'relay_swimmer_4_gender'], axis=1, inplace=True)
tokyo2020 = tokyo2020[tokyo2020['dq'] == 0]
tokyo2020.drop(['dq'], axis=1, inplace=True)


st.dataframe(tokyo2020, use_container_width=True)



