import pandas as pd 
import numpy as np 
import streamlit as st
from streamlit_folium import folium_static
import app.graph as graph
import app.dataUtil as dtUtils
import app.dataFrameUtils as dfUtils

st.set_page_config(page_title='EDA - JAG',
                    page_icon =None,
                    layout='wide',
                    initial_sidebar_state="expanded")

st.title("Análisis de los delitos penales cometidos en España")

df_delito = dtUtils.cargarDelito()
#df_poblacion = dtUtils.cargarPoblacion()
df_crimen_pob = dtUtils.cargarCrimenPob()
anyos = list(map(lambda x: int(x),dfUtils.getAnyos()))

selectMenu = st.sidebar.selectbox(
    'Menú',
    ('Home', 'España','Comunidades Autónomas')
)
filterAnyo = st.sidebar.slider(
    'Filtro por año:',
    min(anyos), max(anyos), (min(anyos),max(anyos))
)

if selectMenu == 'España':
   
    selectEvol = st.selectbox(
        '¿Cómo ver la evolución trimestral?',
        ('Total España', 'Agregada por tipo delito')
    )

    if selectEvol == 'Total España':

        fig = graph.evolNacional(df_delito,filterAnyo)

        st.plotly_chart(fig)
    else:
    
        fig2= graph.evolucionDelitos(df_delito,filterAnyo)

        st.plotly_chart(fig2)

        fig3 = graph.rankingDelitosEspana(df_delito,filterAnyo)

        st.plotly_chart(fig3)
elif selectMenu == 'Comunidades Autónomas':

    selectIndicadorCCAA = st.selectbox(
        '¿Tipo de indicador?',
        ('índice delictivo CCAA vs España', 'Ranking CCAA','Ranking CCAA por delito')
    )

    if selectIndicadorCCAA == 'índice delictivo CCAA vs España':
        fig5 = graph.indiceDelincuencia(df_crimen_pob,filterAnyo)
        st.plotly_chart(fig5)

    elif selectIndicadorCCAA == 'Ranking CCAA':
        selectFormato = st.selectbox(
        'Presentación:',
        ('Ranking','Mapa')
        )
        if selectFormato == "Ranking":
            fig4 = graph.rankingCCAAHab(df_crimen_pob,filterAnyo)
            st.plotly_chart(fig4)
        elif selectFormato == 'Mapa':
            fig7 = graph.mapSpainCCAA(df_crimen_pob,filterAnyo)
            folium_static(fig7)
    elif selectIndicadorCCAA == 'Ranking CCAA por delito':
        
        delitos = dfUtils.getListaTipodelitos(df_crimen_pob)

        selectDelito = st.selectbox(
        '¿Tipo de Delito?',
        tuple(delitos)
        )
        #Muestra todos los rankings
        #for delito in delitos:
            #fig6 = graph.rankingDelitoCCAAHab(df_crimen_pob,delito)
            #st.plotly_chart(fig6)
        
        fig6 = graph.rankingDelitoCCAAHab(df_crimen_pob,selectDelito,filterAnyo)
        st.plotly_chart(fig6)
    
elif selectMenu =='Home':
    pass