import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Resultados de Natação em Tóquio 2020",
     page_icon="🏊‍♂️",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={}
 )


st.header("Resultados de Natação em Tóquio 2020")
st.image("https://news.cgtn.com/news/2021-08-01/McKeon-Dressel-shine-at-Tokyo-Olympics-swimming-events-12mOEAiUkIE/img/2a0c7b6dd09d4a1399b06643328818bd/2a0c7b6dd09d4a1399b06643328818bd-1920.png")

st.subheader("Sobre o projeto")
st.write('Projeto do Trabalho de Conclusão da Disciplina de Análise e Visualização de Dados da Pós-Graduação em Engenharia e Análise de Dados da CESAR School intitulado "Resultados de Natação em Tóquio 2020", desenvolvido pelos discentes Anísio Pereira Batista Filho, Isabel Francine Mendes e Ruy Ovidio Perreli de Melo.')

st.subheader("Sobre o dataset")
st.write("Resultados completos das competições de natação (masculino e feminino, em piscina) nos Jogos Olímpicos de 2020, realizados em Tóquio, Japão. Cada linha representa o desempenho de um atleta (individual ou em grupo), em uma prova de natação.")
st.write("Kaggle: https://www.kaggle.com/datasets/gregpilgrim/tokyo-2020-swimming-results")

st.subheader("Projeto")
st.write("GitHub: https://github.com/anisiobfilho/cesar-streamlit-project")