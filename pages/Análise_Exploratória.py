import streamlit as st
import pandas as pd
import numpy as np
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

tokyo2020 = carrega_base("data/tokyo_2020_swim.csv")

st.subheader("Base de Dados Pré-processada")

tokyo2020 = tokyo2020.dropna(subset=['place', 'lane'])
tokyo2020['place'] = tokyo2020['place'].astype(int)
tokyo2020['lane'] = tokyo2020['lane'].astype(int)
replace_dict = {'USA - United States of America': 'USA', 'ITA - Italy': 'ITA', 'AUS - Australia': 'AUS',
                'CAN - Canada':'CAN', 'HUN - Hungary': 'HUN', 'FRA - France':'FRA', 'ROC - ROC':'ROC', 'BRA - Brazil':'BRA', 'SRB - Serbia':'SRB',
                'POL - Poland':'POL', 'JPN - Japan':'JPN', 'GRE - Greece':'GRE', 'GBR - Great Britain':'GBR', 'NED - Netherlands':'NED',
                'SUI - Switzerland':'SUI', 'GER - Germany':'GER', "CHN - People's Republic of China":'CHN', 'BLR - Belarus':'BLR','ISR - Israel':'ISR',
                'KOR - Republic of Korea':'KOR', 'IRL - Ireland':'IRL','SWE - Sweden':'SWE', 'DEN - Denmark':'DEN', 'HKG - Hong Kong, China':'HKG','CZE - Czech Republic':'CZE',
                'RSA - South Africa':'RSA', 'ESP - Spain':'ESP','TUR - Turkey':'TUR', 'NZL - New Zealand':'NZL' }
tokyo2020['team'] = tokyo2020['team'].replace(replace_dict)
tokyo2020 = tokyo2020[~tokyo2020['team'].isin(['0.65', '0.66'])]
tokyo2020.drop(['relay_swimmer_1', 'relay_swimmer_2', 'relay_swimmer_3','relay_swimmer_4', 'relay_swimmer_1_gender', 'relay_swimmer_2_gender', 'relay_swimmer_3_gender', 'relay_swimmer_4_gender'], axis=1, inplace=True)
tokyo2020 = tokyo2020[tokyo2020['dq'] == 0]
tokyo2020.drop(['dq'], axis=1, inplace=True)

st.dataframe(tokyo2020, use_container_width=True)


st.subheader("Tempo de reação: Eliminatória Women 50 Freestyle")

tempoReacao = tokyo2020[(tokyo2020['event']== "women 50m freestyle") & (tokyo2020.heat.str.startswith('heat_'))]
fig1 = px.scatter(tempoReacao, 
                  x="reaction_time", 
                  y="time", 
                  trendline="ols", 
                  title="Tempo de reação nas eliminatórias de 50m livre para mulheres")
st.plotly_chart(fig1, use_container_width=True)


st.subheader("Finalistas Men 400m Individual Medley")

medley = pd.DataFrame(tokyo2020[(tokyo2020['heat']=='final') & (tokyo2020['event']=='men 400m individual medley')])
data = {
    'Atleta': medley[('place')],
    'split_50': medley['split_50'],
    'split_100': medley['split_100'],
    'split_150': medley['split_150'],
    'split_200': medley['split_200'],
    'split_250': medley['split_250'],
    'split_300': medley['split_300'],
    'split_350': medley['split_350'],
    'split_400': medley['split_400'],
}
dfMedley2 = pd.DataFrame(data)
fig2 = px.parallel_coordinates(dfMedley2, 
                               color="Atleta", 
                               dimensions=['Atleta','split_50', 'split_100', 'split_150', 'split_200', 'split_250', 'split_300', 'split_350', 'split_400'], 
                               color_continuous_scale=px.colors.sequential.Turbo, 
                               color_continuous_midpoint=4)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Número e tipo de medalhas ganhadas e agrupadas por país")

final_df = tokyo2020[tokyo2020['heat'] == 'final']
first_place_df = final_df[final_df['place'] == 1]
second_place_df = final_df[final_df['place'] == 2]
third_place_df = final_df[final_df['place'] == 3]
teamGoldMedal = first_place_df.groupby('team').size().sort_values(ascending=False)
teamSilverMedal = second_place_df.groupby('team').size().sort_values(ascending=False)
teamBronzeMedal = third_place_df.groupby('team').size().sort_values(ascending=False)
teams_gold = np.array(first_place_df['team'].values)
teams_silver = np.array(second_place_df['team'].values)
teams_bronze = np.array(third_place_df['team'].values)
concat_teams = np.concatenate((teams_gold, teams_silver, teams_bronze))
unique_teams = np.unique(concat_teams)

medal_counts = pd.DataFrame({
    'Team': unique_teams,
    'Gold': teamGoldMedal.reindex(unique_teams).values,
    'Silver': teamSilverMedal.reindex(unique_teams).values,
    'Bronze': teamBronzeMedal.reindex(unique_teams).values
})
medal_counts['Total'] = medal_counts.sum(axis=1)
medal_counts = medal_counts.sort_values(by=['Total','Gold','Silver','Bronze'], ascending=False)
medal_counts = medal_counts.drop('Total', axis=1)
df_melted = pd.melt(medal_counts, id_vars=['Team'], var_name='Medal', value_name='Count')
fig3 = px.bar(df_melted, x='Team', y='Count', color='Medal', color_discrete_sequence=['gold','silver', '#cd7f32'])
fig3.update_layout(
    title='Total Medals by Country',
    xaxis_title='Country',
    yaxis_title='Number of Medals',
    legend_title='Medal',
    legend=dict(title='Medal', orientation='h', y=1.1, x=0.5),
    barmode='group',
    showlegend=True
)
st.plotly_chart(fig3, use_container_width=True)