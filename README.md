# EDA_delitosEspana
EDA y aplicación sobre los delitos en España por municipios de 2016-2020

## Datos
Los datos se obtienen, principalmente:
* De la página de datos abiertos del Ministerio del Interior, concretamente del portal estadístico de Criminalidad [web](https://estadisticasdecriminalidad.ses.mir.es/publico/portalestadistico/portal/balances.html)
* Datos demográficos a nivel municipio obtenidos de la página del INE [web](https://www.ine.es/dynt3/inebase/es/index.htm?padre=517&capsel=525)

## Librerias:
Para el tratamiento de la información:
  * pandas
  * numpy
  * csv
  * json

Para los gráficos:
  * plotly.express
  * from plotly.subplots import make_subplots
  * plotly.graph_objects
  * folium
 
 Para la aplicación:
  * import streamlit as st
  * from streamlit_folium import folium_static
