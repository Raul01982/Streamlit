import streamlit as st
import pandas as pd
import seaborn as sns

st.title('Hello Wilders, welcome to my application!')

st.write("I enjoy to discover stremalit possibilities")

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/weather2019.csv"
df_weather = pd.read_csv(link)
df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
st.write(df_weather)

st.line_chart(df_weather['MAX_TEMPERATURE_C'])

df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
graph = sns.heatmap(df_weather.drop(columns='OPINION').corr(), 
								center=0,
								cmap = sns.color_palette("vlag", as_cmap=True)
								)

st.pyplot(graph.figure)
