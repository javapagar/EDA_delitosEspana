import pandas as pd 
import numpy as np 
import streamlit as st
import app.graph as graph

st.set_page_config(page_title='EDA',
                    page_icon =None,
                    layout='centered',
                    initial_sidebar_state="expanded")

st.title("Delitos penales en España")

df_delito = pd.read_csv('./data/clean/delitos.csv')
df_poblacion = pd.read_csv ('./data/clean/poblacion.csv')
df_crimen_pob = pd.read_csv('./data/clean/crimen_pob.csv')

fig = graph.evolNacional(df_delito)

st.plotly_chart(fig)