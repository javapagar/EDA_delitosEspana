import pandas as pd 
import plotly.express as px
import app.dataFrameUtils as dfUtils

def evolNacional(df):
    qcolumns = dfUtils.getQColumns(df)
    
    comunidadQColumns = ['Comunidad',*qcolumns]

    total_espana = dfUtils. getNacional(df)
    
    #Delitos Totales
    total_espana_graph =total_espana[comunidadQColumns]

    total_espana_graph = pd.melt(total_espana_graph,id_vars=['Comunidad'],value_vars=qcolumns, var_name='Trimestre',value_name='Criminalidad')

    total_espana_graph.Trimestre =pd.to_datetime(total_espana_graph.Trimestre)
    fig = px.line(total_espana_graph, x="Trimestre", y='Criminalidad',
                hover_data={"Trimestre": "|%q trimestre-%Y"},
              )
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(dtick="M3",tickformat="%q-%Y", tickangle = 45)
    fig.update_layout(
                    title="<b>Evolución Trimestral del crimen en España (2016-2020)</b>")

    return fig
    #fig.show()