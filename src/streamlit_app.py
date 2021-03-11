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
    ('Home', 'Indicadores','España','Comunidades Autónomas')
)

if selectMenu != 'Home' and selectMenu != 'Indicadores':
    st.sidebar.markdown('-------')

    filterAnyo = st.sidebar.slider(
        'Filtro por año:',
        min(anyos), max(anyos), (min(anyos),max(anyos))
    )

legend_exppander= st.sidebar.beta_expander('Códigos de delitos')
legend_exppander.markdown("1.-Homicidios dolosos y asesinatos consumados")
legend_exppander.markdown("2.-Homicidios dolosos y asesinatos en grado tentativa")
legend_exppander.markdown("3.-Delitos graves y menos graves de lesiones y riña tumultuaria")
legend_exppander.markdown("4.-Secuestro")
legend_exppander.markdown("5.-Delitos contra la libertad e indemnidad sexual")
legend_exppander.markdown("6.-Robos con violencia e intimidación")
legend_exppander.markdown("7.- Robos con fuerza en domicilios, establecimientos y otras instalaciones")
legend_exppander.markdown("8.-Hurtos")
legend_exppander.markdown("9.-Sustracciones de vehículos")
legend_exppander.markdown("10.-Tráfico de drogas Resto de infracciones penales")

if selectMenu == 'España':
   
    selectEvol = st.selectbox(
        '¿Cómo ver la evolución trimestral?',
        ('Total España', 'Agregada por tipo delito')
    )

    if selectEvol == 'Total España':
        df =dfUtils. getNacional(df_delito)
        fig = graph.evolTrimestral(df,filterAnyo)

        st.plotly_chart(fig)
    else:
        df = dfUtils.getEspanaTipoDelito(df_delito)
        
        fig2= graph.evolucionDelitos(df,filterAnyo)

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
    elif selectIndicadorCCAA =='Evolución trimestral CCAA':
        comunidades = ['Selecciona Comunidad'] + dfUtils.getListComunidades(df_crimen_pob)
        selectComunidad = st.selectbox(
            'Comunidad:',
            tuple(comunidades)
            )
        if selectComunidad != 'Selecciona Comunidad':
            
            dfComunidad = dfUtils.getComunidad(df_crimen_pob,selectComunidad)
            evol = graph.evolTrimestral(dfComunidad,filterAnyo)
            st.plotly_chart(evol)

            df = dfUtils.getComuniadTipoDelito(df_delito,selectComunidad)
            st.write(df)
            evolDel= graph.evolucionDelitos(df,filterAnyo)

            st.plotly_chart(evolDel)
elif selectMenu =='Home':
    with st.beta_container():
        with st.beta_container():
            st.markdown('## Objetivo')
        with st.beta_container():
            st.write('Esta aplicación quiere crear un espacio donde se pueda analizar el estado \
            y la evolución de la criminalidad, tanto a nivel nacional como a nivel \
            de comunidad autónoma, de forma total o agrupada por tipo de delito de forma interactiva.')

    with st.beta_container():
        with st.beta_container():
            st.markdown('## Fuentes de datos')
            with st.beta_container():
                col1, col2 = st.beta_columns((1,2))
                col1.image('./app/img/logo_sec.png')
                col2.markdown('  ')
                col2.write("Portal estadístico de Criminalidad, que forma parte de los datos abiertos del Ministerio del Interior, \
                concretamente del portal estadístico de Criminalidad  ")
                col2.write("Los datos del Ministerio ofrecen el recuento de crímenes categorizados por tipología en diferentes niveles, \
                nacional, comunidad autónoma, provincia y municipios de más de 30.000 habitantes. Estos datos se presentan en una \
                    serie temporal trimestral, y, de momento, comprende el periodo de 2016 a 2020.")
            with st.beta_container():
                col1, col2 =st.beta_columns((2,1))
                col2.image('./app/img/logo_ine.png')
                col1.markdown('  ')
                col1.write("Datos demográficos obtenidos de la página del INE a nivel municipio y por año.")
elif selectMenu =='Indicadores':
    with st.beta_container():
        with st.beta_container():
            st.markdown('## Estadísticas e indicadores')
        with st.beta_container():
            st.write("A nivel Nacional:")
            with st.beta_container():
                st.markdown('* Evolución temporal por trimestre del número total de delitos cometidos en España:  \
                recuento del número total de delitos')
                st.markdown('* Evolución temporal por trimestre del número total de delitos cometidos en España agrupados por tipo de delito:  \
                recuento del número total de delitos')
                st.markdown('* Ranking de la tipología de delitos en España:  \
                recuento del número total de delitos')
        with st.beta_container():
            st.write("A nivel autonómico:")
            st.markdown('* Ranking de comunidades: tasa media de delitos del periodo')
            st.markdown('* Índice delictivo por cada 1000.000 habitantes: índice de criminalidad')
            st.markdown('* Ranking de CCAA por cada tipo de delito: tasa media de delitos del periodo')
    
    



#css
st.markdown('''<style>h1{color: white;background-color: cornflowerblue;text-align: center;padding: 30px;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>h2{color: cornflowerblue;border-bottom: 5px solid cornflowerblue;padding: 10px;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>html{font-family: arial,sans-serif;font-size:large;}''',unsafe_allow_html=True)
st.markdown('''<style>.svg{width:100%;}''',unsafe_allow_html=True)