import pandas as pd 
import numpy as np 
import streamlit as st
from streamlit_folium import folium_static
import app.graph as graph
import app.dataUtil as dtUtil

st.set_page_config(page_title='EDA - JAG',
                    page_icon =None,
                    layout='wide',
                    initial_sidebar_state="expanded")

st.title("Análisis de los delitos penales cometidos en España")

df_delito = dtUtil.cargarDelito()
#df_poblacion = dtUtil.cargarPoblacion()
df_crimen_pob = dtUtil.cargarCrimenPob()

selectMenu = st.sidebar.selectbox(
    'Menú',
    ('Home', 'España','C. Autónomas')
)

if selectMenu == 'España':
    selectEvol = st.selectbox(
        '¿Cómo ver la evolución trimestral?',
        ('Total', 'Por tipo delito')
    )

    if selectEvol == 'Total':

        fig = graph.evolNacional(df_delito)

        st.plotly_chart(fig)
    else:
    
        fig2= graph.evolucionDelitos(df_delito)

        st.plotly_chart(fig2)

        fig3 = graph.rankingDelitosEspana(df_delito)

        st.plotly_chart(fig3)
elif selectMenu == 'C. Autónomas':

    selectIndicadorCCAA = st.selectbox(
        '¿Tipo de indicador?',
        ('índice delictivo', 'Ranking CCAA','Ranking CCAA por delito')
    )
    if selectIndicadorCCAA == 'índice delictivo':
        fig5 = graph.indiceDelincuencia(df_crimen_pob)
        st.plotly_chart(fig5)

    elif selectIndicadorCCAA == 'Ranking CCAA':

        fig4 = graph.rankingCCAAHab(df_crimen_pob)
        st.plotly_chart(fig4)
        
        fig7 = graph.mapSpainCCAA(df_crimen_pob)
        folium_static(fig7)
    elif selectIndicadorCCAA == 'Ranking CCAA por delito':
        
        delitos = graph.getListDelitos(df_crimen_pob)

        selectDelito = st.selectbox(
        '¿Tipo de Delito?',
        tuple(delitos)
    )
        #Muestra todos los rankings
        #for delito in delitos:
            #fig6 = graph.rankingDelitoCCAAHab(df_crimen_pob,delito)
            #st.plotly_chart(fig6)
        
        fig6 = graph.rankingDelitoCCAAHab(df_crimen_pob,selectDelito)
        st.plotly_chart(fig6)
    
elif selectMenu =='Home':
    pass