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
st.sidebar.image("img/mascot.png")

st.cache_resource.clear()

## MAIN
st.header("Análise de Dados")

@st.cache_resource
def carrega_base(path):
    data = pd.read_csv(path, sep=",", low_memory=True)
    return data

tokyo2020 = carrega_base("data/tokyo_2020_swim.csv")

st.subheader("Base de dados pré-processada")

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

st.subheader("Tempo de reação")
col1, col2 = st.columns([1,3])
with col1:
    event_selected = st.selectbox('Selecione o evento que você gostaria de analisar?', (tokyo2020.event.unique()), key=1)
with col2:
    tempoReacao = tokyo2020[(tokyo2020['event']== event_selected) & (tokyo2020.heat.str.startswith('heat_'))]
    fig1 = px.scatter(tempoReacao, 
                    x="reaction_time", 
                    y="time", 
                    trendline="ols", 
                    title=f"Tempo de reação no evento: {event_selected}")
    st.plotly_chart(fig1, use_container_width=True)

st.subheader("Eventos finais")
col3, col4 = st.columns([1, 3])

with col3:
    event_selected2 = st.selectbox('Selecione o evento que você gostaria de analisar?', list(tokyo2020['event'].unique()), key=2)

with col4:
    medley = pd.DataFrame(tokyo2020[(tokyo2020['heat'] == 'final') & (tokyo2020['event'] == event_selected2)])
    split_columns = [col for col in medley.columns if col.startswith('split_')]

    # Removendo colunas que têm todos os valores nulos
    medley = medley.dropna(subset=split_columns, how='all')

    # Criando dinamicamente as colunas para os splits disponíveis no evento
    data = {'Atleta': medley['place']}
    for split_col in split_columns:
        data[split_col] = medley[split_col]

    dfMedley2 = pd.DataFrame(data)
    dfMedley2.dropna(how='all', axis=1, inplace=True)
    fig2 = px.parallel_coordinates(dfMedley2,
                                   color="Atleta",
                                   dimensions=dfMedley2.columns,
                                   color_continuous_scale=px.colors.sequential.Turbo,
                                   color_continuous_midpoint=4,
                                   title=f"Evento final: {event_selected2}")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Resultado final das medalhas conquistadas por país")
medals_array = ["Total", "Gold", "Silver", "Bronze"]

medal = st.radio(
    "Choose a medal to display in the chart",
    medals_array,
    horizontal=True,
)

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
medal_counts['Total'] = medal_counts.sum(numeric_only= True, axis=1)

color_sequence = []
if medal == 'Total':
    medal_counts = medal_counts.sort_values(by=medals_array, ascending=False)
    medal_counts.drop('Total', axis=1, inplace=True)
    color_sequence = ['Gold','Silver', '#cd7f32']
else:
    medals_filtered = [x for x in medals_array if (x != medal or x == 'Total')]
    medal_counts.drop(medals_filtered, axis=1, inplace=True)
    medal_counts = medal_counts.sort_values(by=medal, ascending=False)
    if medal == 'Bronze':
        color_sequence=['#cd7f32']
    else:
        color_sequence=[medal]

df_melted = pd.melt(medal_counts, id_vars=['Team'], var_name='Medal', value_name='Count')
fig3 = px.bar(df_melted, x='Team', y='Count', color='Medal', color_discrete_sequence=color_sequence)
fig3.update_layout(
    title=medal+' Medals by Country',
    xaxis_title='Country',
    yaxis_title='Number of Medals',
    legend_title='Medal',
    legend=dict(title='Medal', orientation='h', y=1.1, x=0.5),
    barmode='group',
    showlegend=True
)
st.plotly_chart(fig3, use_container_width=True)