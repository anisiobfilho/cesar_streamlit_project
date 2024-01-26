import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Resultados de Natação em Tóquio 2020",
     page_icon="🏊‍♂️",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={}
 )
st.sidebar.image("img/mascot.png")

st.header("Resultados de Natação em Tóquio 2020")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Sobre o projeto")
    st.write('Projeto do Trabalho de Conclusão da Disciplina de Análise e Visualização de Dados da Pós-Graduação em Engenharia e Análise de Dados da CESAR School intitulado "Resultados de Natação em Tóquio 2020", desenvolvido pelos discentes Anísio Pereira Batista Filho, Isabel Francine Mendes e Ruy Ovidio Perreli de Melo.')

    st.subheader("Sobre o dataset")
    st.write("Resultados completos das competições de natação (masculino e feminino, em piscina) nos Jogos Olímpicos de 2020, realizados em Tóquio, Japão. Cada linha representa o desempenho de um atleta (individual ou em grupo), em uma prova de natação.")
    st.write("Kaggle: https://www.kaggle.com/datasets/gregpilgrim/tokyo-2020-swimming-results")

    st.subheader("Projeto")
    st.write("GitHub: https://github.com/anisiobfilho/cesar_streamlit_project")

with col2:
    st.image("img/logo.png")
    st.image("img/event.png")