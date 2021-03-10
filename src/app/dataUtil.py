import pandas as pd
import streamlit as st

#cargar datos
@st.cache(suppress_st_warning=True)
def cargarDelito():
    return pd.read_csv('./data/clean/delitos.csv')
@st.cache(suppress_st_warning=True)
def cargarPoblacion():
    return pd.read_csv ('./data/clean/poblacion.csv')
@st.cache(suppress_st_warning=True)
def cargarCrimenPob():
    return pd.read_csv('./data/clean/crimen_pob.csv')