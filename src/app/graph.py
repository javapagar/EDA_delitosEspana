import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import app.dataFrameUtils as dfUtils

def test(df):
  return dfUtils.getEspanaTipoDelito(df)

def evolNacional(df,withDelito=None):
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


def evolucionDelitos(df):
  qcolumns = dfUtils.getQColumns(df)
  
  espana_tipo_delito_graph1 = dfUtils.getEspanaTipoDelito(df)

  delitQColumns = ['code','Delito',*qcolumns]

  espana_tipo_delito_graph1 = espana_tipo_delito_graph1[delitQColumns]

  espana_tipo_delito_graph1 = pd.melt(espana_tipo_delito_graph1,id_vars=['code','Delito'],value_vars=qcolumns, var_name='Trimestre',value_name='Criminalidad')

  espana_tipo_delito_graph1 = espana_tipo_delito_graph1.pivot(index='Trimestre',columns='Delito',values='Criminalidad')

  espana_tipo_delito_graph1 = espana_tipo_delito_graph1.reset_index()

  espana_tipo_delito_graph1.Trimestre =pd.to_datetime(espana_tipo_delito_graph1.Trimestre)

  #tit_graph = tuple(espana_tipo_delito_graph1.columns[1:])

  traduce_delitos = ('Robos con fuerza en domicilios','Contra la libertad e indemnidad sexual','Lesiones y riña tumultuaria','Homicidios y asesinatos consumados','Homicidios y asesinatos tentativa','Hurtos', 'Robos con violencia e intimidación','Secuestro', 'Sustracciones de vehículos', 'Tráfico de drogas')

  fig = make_subplots(rows=5, 
                      cols=2,
                      subplot_titles=traduce_delitos,
                      shared_xaxes=True)

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y= espana_tipo_delito_graph1.iloc[:,1]),
      row=1, col=1
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y=espana_tipo_delito_graph1.iloc[:,2]),
      row=1, col=2
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y= espana_tipo_delito_graph1.iloc[:,3]),
      row=2, col=1
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y=espana_tipo_delito_graph1.iloc[:,4]),
      row=2, col=2
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y= espana_tipo_delito_graph1.iloc[:,5]),
      row=3, col=1
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y=espana_tipo_delito_graph1.iloc[:,6]),
      row=3, col=2
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y= espana_tipo_delito_graph1.iloc[:,7]),
      row=4, col=1
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y=espana_tipo_delito_graph1.iloc[:,8]),
      row=4, col=2
  )
  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y= espana_tipo_delito_graph1.iloc[:,9]),
      row=5, col=1
  )

  fig.add_trace(
      go.Scatter(x=espana_tipo_delito_graph1.iloc[:,0], y=espana_tipo_delito_graph1.iloc[:,10]),
      row=5, col=2
  )
  fig.update_layout(height=800, width=1000, title_text="Evolucion trimestral por tipo de delitos")
  fig.update_traces(mode="markers+lines")
  fig.update_xaxes(dtick="M3",tickformat="%q-%Y")
  fig.update_layout(showlegend=False)
  fig.update_xaxes(
      dtick="M3",
      tickangle= 45
      )
  return fig

def rankingDelitosEspana(df):

  espana_tipo_delito_graph2 = dfUtils.getEspanaTipoDelito(df)
  
  total_columns = ['code','Delito','Total','MediaTotal']

  espana_tipo_delito_graph2 = espana_tipo_delito_graph2[total_columns]


  espana_tipo_delito_graph2 = espana_tipo_delito_graph2.sort_values('MediaTotal')

  fig = px.bar(espana_tipo_delito_graph2, y='Delito', x='MediaTotal', text='MediaTotal', title='Ranking delitos penales en España (2016-2020)', width =900)
  fig.update_traces(texttemplate='%{text:.3s}')
  fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
  
  return fig

def rankingCCAAHab(df):

  ene_dic_columns = dfUtils.getEneDicColumns(df)
  pob_columns = dfUtils.getPobColumns(df)

  comunidadesUnionCrimenPob = df.groupby(['Comunidad'])[[*ene_dic_columns,*pob_columns]].sum()

  comunidadesUnionCrimenPob = dfUtils.calculateMediaDelitoPob(comunidadesUnionCrimenPob,100000)

  comunidadesUnionCrimenPob = comunidadesUnionCrimenPob.sort_values('MediaDelitosPob')

  fig = px.bar(comunidadesUnionCrimenPob, y='Comunidad', x='MediaDelitosPob', text='MediaDelitosPob', title='Ranking CCAA tasa Delitos por cada 100.000 habitantes en España (2016-2020)',height = 600,  width =900)
  fig.update_traces(texttemplate='%{text:.3s}')
  fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

  return fig

def indiceDelincuencia(df):

  ene_dic_columns = dfUtils.getEneDicColumns(df)
  pob_columns = dfUtils.getPobColumns(df)

  nacionalUnionCrimenPob = df.groupby(['code','Delito'])[[*ene_dic_columns,*pob_columns]].sum()

  nacionalUnionCrimenPob =dfUtils.calculateMediaDelitoPob(nacionalUnionCrimenPob,100000)

  comunidadesUnionCrimenPob = df.groupby(['Comunidad','code','Delito'])[[*ene_dic_columns,*pob_columns]].sum()

  comunidadesUnionCrimenPob = dfUtils.calculateMediaDelitoPob(comunidadesUnionCrimenPob,100000)

  comunidades = list(set(df['Comunidad']))

  i,j=1,1

  fig = make_subplots(rows=7, 
                      cols=3,
                      subplot_titles=comunidades,
                      
                      )

  for comunidad in comunidades:
      df_comunidad = comunidadesUnionCrimenPob[comunidadesUnionCrimenPob.Comunidad.str.contains(comunidad, regex=False)]
      df_comunidad = pd.merge(df_comunidad,nacionalUnionCrimenPob, left_on = ['code','Delito'],right_on=['code','Delito'])
      df_comunidad['IDE'] = round(df_comunidad.MediaDelitosPob_x / df_comunidad.MediaDelitosPob_y,3)
      df_comunidad["Color"] = np.where(df_comunidad["IDE"]>1, 'red', 'green')

      fig.add_trace(
          go.Bar(name='IDE',
              x=df_comunidad.code,
              y=df_comunidad.IDE,
              hovertemplate = "Delito:%{x}: <br>IDE: %{y}",
              marker_color=df_comunidad.Color),
              row=i, col=j)
      j +=1
      if j == 4:
          i +=1
          j=1

  fig.update_layout(height=800, width=1000, title_text="Índice delictivo por cada 100.000 habitantes comunidad vs España (2016-2020)")    
  fig.update_layout(barmode='stack')
  fig.update_layout(showlegend=False)
  
  return fig