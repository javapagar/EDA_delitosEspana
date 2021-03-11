import streamlit as st
import pandas as pd
#listas
def getListaTipodelitos(df):
    return list(set(df.Delito))

def getListComunidades(df):

    return sorted(list(set(df.Comunidad)))

#columnas
@st.cache(suppress_st_warning=True)
def getAnyos():
    return ['2016','2017','2018','2019','2020']

def getQColumns(df):
    return df.columns[df.columns.str.contains('Q')]

def getEneDicColumns(df):
    return df.columns[df.columns.str.contains('Enero-diciembre')]

def getPobColumns(df):
    return df.columns[df.columns.str.contains('POB')]

#máscaras
def getNacional(df):
    return df[df.Comunidad.str.contains('NACIONAL') & df.Delito.str.contains('TOTAL')]

def getComunidad(df,comunidad):
    return df[df.Comunidad.str.contains(comunidad,regex=False)]

def getEspanaTipoDelito(df):
    return df[df.Comunidad.str.contains('NACIONAL') & ~ df.code.str.contains('code') & ~ df.code.str.contains('5.') & ~ df.code.str.contains('7.')]

def getComuniadTipoDelito(df,comunidad):
    return df[df.Nivel.str.contains('Comunidad',regex =False) & df.Comunidad.str.contains(comunidad,regex =False) & ~ df.code.str.contains('code') & ~ df.code.str.contains('5.') & ~ df.code.str.contains('7.')]

def filtrarAnyos(df,anyos):
    return df[df['Anyo'].isin(anyos)] 

#Funciones tratan df
def addTasaDelitoPob(df, anyo, habitantes):
    aaaa = str(anyo)
    columnsTasaPob=df.columns[df.columns.str.contains(aaaa)]
    df['Delito/pob_'+ aaaa]=(df[columnsTasaPob[0]] / df[columnsTasaPob[1]]) * int(habitantes)


def calculateMediaDelitoPob(df,habitantes, anyos=None):

    if anyos == None:
        anyos =getAnyos()

    for anyo in anyos:
        addTasaDelitoPob(df,anyo,habitantes)

    columnsDelitoPob = df.columns[df.columns.str.contains('Delito/pob')]
    
    tot = 0
    for col in columnsDelitoPob:
        tot += df[col]
    
    df['MediaDelitosPob'] =tot/len(columnsDelitoPob)
    df.sort_values('MediaDelitosPob',ascending = False)
    df = df.reset_index()
    return df

def addTotalColumn(df):
    columns =getEneDicColumns(df)
    df['Total'] = 0
    for column in columns:
        df['Total'] += df[column]
    return df

def delEneDicColumn(df,anyos):
    columnsFilter = list(map(lambda x:'Enero-diciembre '+str(x),anyos))
    columnsAll = getEneDicColumns(df)
    for column in columnsAll:
        if not column in columnsFilter:
            del(df[column])
    return df