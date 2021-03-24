import pandas as pd
import numpy as np
import json
import folium as folium
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import app.dataFrameUtils as dfUtils

def evolTrimestral(df,filterAnyo,withDelito=None):
    
    anyos =range(filterAnyo[0],filterAnyo[1]+1)
    
    qcolumns = dfUtils.getQColumns(df)
    
    comunidadQColumns = ['Comunidad',*qcolumns]

    total_espana =df.groupby('Comunidad').sum()
    total_espana = total_espana.reset_index()
    #total_espana = dfUtils. getNacional(df)
    
    #Delitos Totales
    total_espana_graph =total_espana[comunidadQColumns]

    total_espana_graph = pd.melt(total_espana_graph,id_vars=['Comunidad'],value_vars=qcolumns, var_name='Trimestre',value_name='Criminalidad')

    total_espana_graph['Anyo'] =list(map(lambda x: pd.to_datetime(x).year,total_espana_graph['Trimestre']))

    total_espana_graph = dfUtils.filtrarAnyos(total_espana_graph,anyos)

    total_espana_graph.Trimestre =pd.to_datetime(total_espana_graph.Trimestre)
    fig = px.line(total_espana_graph, x="Trimestre", y='Criminalidad',
                hover_data={"Trimestre": "|%q trimestre-%Y"},
                width=1000, height=400
              )
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(dtick="M3",tickformat="%q -%Y", tickangle = 45)
    fig.update_layout(
                    title="<b>Evolución Trimestral del crimen</b>")
    fig.update_layout(hovermode="x")

    return fig
    #fig.show()

def evolucionDelitos(df,filterAnyo):
    anyos =range(filterAnyo[0],filterAnyo[1]+1)

    qcolumns = dfUtils.getQColumns(df)
    
    #espana_tipo_delito_graph1 = dfUtils.getEspanaTipoDelito(df)
    espana_tipo_delito_graph1 =df.groupby(['code','Delito']).sum()
    espana_tipo_delito_graph1=espana_tipo_delito_graph1.reset_index()

    delitQColumns = ['code','Delito',*qcolumns]

    espana_tipo_delito_graph1 = espana_tipo_delito_graph1[delitQColumns]

    espana_tipo_delito_graph1 = pd.melt(espana_tipo_delito_graph1,id_vars=['code','Delito'],value_vars=qcolumns, var_name='Trimestre',value_name='Criminalidad')

    espana_tipo_delito_graph1['Anyo'] =list(map(lambda x: pd.to_datetime(x).year,espana_tipo_delito_graph1['Trimestre']))
    
    espana_tipo_delito_graph1 = dfUtils.filtrarAnyos(espana_tipo_delito_graph1,anyos)
    
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
    fig.update_layout(showlegend=False)
    fig.update_xaxes(
        tickformat="%q-%Y",
        dtick="M3",
        tickangle= 45
        )
    fig.update_layout(hovermode="x")
    return fig

def rankingDelitosEspana(df,filterAnyo):
    anyos =range(filterAnyo[0],filterAnyo[1]+1)

    espana_tipo_delito_graph2 = dfUtils.getEspanaTipoDelito(df)

    dfUtils.delEneDicColumn(espana_tipo_delito_graph2,anyos)

    espana_tipo_delito_graph2 = dfUtils.addTotalColumn(espana_tipo_delito_graph2)

    total_columns = ['code','Delito','Total','MediaTotal']

    espana_tipo_delito_graph2 = espana_tipo_delito_graph2[total_columns]


    espana_tipo_delito_graph2 = espana_tipo_delito_graph2.sort_values('Total')

    fig = px.bar(espana_tipo_delito_graph2, y='Delito', x='Total', text='Total', title='Ranking delitos penales en España', width =900)
    fig.update_traces(texttemplate='%{text:.3s}')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    return fig


def rankingCCAAHab(df,filterAnyo):
    anyos =range(filterAnyo[0],filterAnyo[1]+1)

    ene_dic_columns = dfUtils.getEneDicColumns(df)
    pob_columns = dfUtils.getPobColumns(df)

    comunidadesUnionCrimenPob = df.groupby(['Comunidad'])[[*ene_dic_columns,*pob_columns]].sum()

    dfUtils.delEneDicColumn(comunidadesUnionCrimenPob,anyos)

    dfUtils.addTotalColumn(comunidadesUnionCrimenPob)

    comunidadesUnionCrimenPob = dfUtils.calculateMediaDelitoPob(comunidadesUnionCrimenPob,100000,anyos)

    comunidadesUnionCrimenPob = comunidadesUnionCrimenPob.sort_values('MediaDelitosPob')

    fig = px.bar(comunidadesUnionCrimenPob, y='Comunidad', x='MediaDelitosPob', text='MediaDelitosPob', title='Ranking CCAA tasa Delitos por cada 100.000 habitantes en España',height = 600,  width =900)
    fig.update_traces(texttemplate='%{text:.3s}')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return fig

def indiceDelincuencia(df, filterAnyo):
    anyos =range(filterAnyo[0],filterAnyo[1]+1)

    ene_dic_columns = dfUtils.getEneDicColumns(df)
    pob_columns = dfUtils.getPobColumns(df)

    nacionalUnionCrimenPob = df.groupby(['code','Delito'])[[*ene_dic_columns,*pob_columns]].sum()

    nacionalUnionCrimenPob =dfUtils.calculateMediaDelitoPob(nacionalUnionCrimenPob,100000,filterAnyo)

    comunidadesUnionCrimenPob = df.groupby(['Comunidad','code','Delito'])[[*ene_dic_columns,*pob_columns]].sum()

    comunidadesUnionCrimenPob = dfUtils.calculateMediaDelitoPob(comunidadesUnionCrimenPob,100000, filterAnyo)

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

    fig.update_layout(height=800, width=1000, title_text="Índice delictivo por cada 100.000 habitantes comunidad vs España")    
    fig.update_layout(barmode='stack')
    fig.update_layout(showlegend=False)
    
    return fig


def rankingDelitoCCAAHab(df,delito,filterAnyo):

    anyos =range(filterAnyo[0],filterAnyo[1]+1)

    ene_dic_columns = dfUtils.getEneDicColumns(df)
    pob_columns = dfUtils.getPobColumns(df)

    comunidadUnionCrimenPob = df.groupby(['Comunidad','code','Delito'])[[*ene_dic_columns,*pob_columns]].sum()

    comunidadUnionCrimenPob = dfUtils.calculateMediaDelitoPob(comunidadUnionCrimenPob,100000,anyos)

    df_filtered = comunidadUnionCrimenPob[comunidadUnionCrimenPob.Delito.str.contains(delito,regex=False)]
    df_filtered = df_filtered.sort_values('MediaDelitosPob')

    fig = px.bar(df_filtered, y='Comunidad', x='MediaDelitosPob', text='MediaDelitosPob', title=delito, height = 600, width =900)

    fig.update_traces(texttemplate='%{text:.3s}')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_xaxes(
            tickangle= 45
            )
    return fig


def mapSpainCCAA(df_crimen_pob, filterAnyo):

    anyos =range(filterAnyo[0],filterAnyo[1]+1)
    ene_dic_columns = dfUtils.getEneDicColumns(df_crimen_pob)
    pob_columns = dfUtils.getPobColumns(df_crimen_pob) 
    #spain_provinces.geojson
    dictComunidades= {'14': 'CIUDAD AUTÓNOMA DE MELILLA',
                        '02': 'ARAGÓN',
                        '07':'CASTILLA Y LEON',
                        '10': 'EXTREMADURA',
                        '18': 'ASTURIAS (PRINCIPADO DE)',
                        '05' : 'CANTABRIA',
                        '19': 'COMUNITAT VALENCIANA',
                        '01' : 'ANDALUCÍA',
                        '17':'PAÍS VASCO',
                        '09': 'CIUDAD AUTÓNOMA DE CEUTA',
                        '08': 'CATALUÑA',
                        '03':'BALEARS (ILLES)',
                        '11': 'GALICIA',
                        '06': 'CASTILLA - LA MANCHA',
                        '15':'MURCIA (REGION DE)',
                        '16':'NAVARRA (COMUNIDAD FORAL DE)',
                        '13' : 'MADRID (COMUNIDAD DE)',
                        '04':'CANARIAS',
                        '12':'RIOJA (LA)'}

    df_codccaa = pd.DataFrame([[key, dictComunidades[key]] for key in dictComunidades.keys()], columns=['codeCCAA','Comunidad'])

    comunidadesUnionCrimenPob = df_crimen_pob.groupby(['Comunidad'])[[*ene_dic_columns,*pob_columns]].sum()
    comunidadesUnionCrimenPob= comunidadesUnionCrimenPob.reset_index()
    df = pd.merge(comunidadesUnionCrimenPob,df_codccaa,left_on='Comunidad',right_on='Comunidad')

    df = dfUtils.calculateMediaDelitoPob(df,100000,anyos)

    #aseguro el encoding del geojson
    with open('./src/app/data/spain_provinces.geojson', "r", encoding="utf-8" ) as response:
        espana = json.load(response)

    # Initialize the map:
    m = folium.Map(location = [36.68548750831435, -5.196817942588608], zoom_start = 5,tiles='cartodbpositron')

    # add tile layers to the map
    # con esto posibilito que luego en el mapa pueda elegir el 'tipo de vista'
    #tiles = ['cartodbpositron','stamenwatercolor','openstreetmap','stamenterrain']

    #for tile in tiles:
        #folium.TileLayer(tile).add_to(m)
    
    # Add the color for the chloropleth:
    choropleth = folium.Choropleth(
    geo_data=espana,
    name='choropleth',
    data=df,
    columns=['codeCCAA', 'MediaDelitosPob'],
    #key_on='feature.properties.cod_ccaa',   # dentro del 'geojson', viendo su estructura de datos rovincias-espanolas.geojson
    key_on='feature.properties.region',   # dentro del 'geojson', viendo su estructura de datos spain_provinces.geojson
    #fill_color='OrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Delitos por cada 100.000 habitantes',
    highlight = True,
    smooth_factor = 0).add_to(m)

    style_function = "font-size: 15px; font-weight: bold"
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_function, labels=False))
    
    #color
    tiles = ['stamenwatercolor','openstreetmap','stamenterrain']
    for tile in tiles:
        folium.TileLayer(tile).add_to(m)
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(m)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(m)
    folium.LayerControl().add_to(m)

    return m