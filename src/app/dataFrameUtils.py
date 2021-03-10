
#listas
def getListaTipodelitos(df):
    return list(set(df.Delito))

#columnas
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

def getEspanaTipoDelito(df):
    return df[df.Comunidad.str.contains('NACIONAL') & ~ df.code.str.contains('code') & ~ df.code.str.contains('5.') & ~ df.code.str.contains('7.')]

#Funciones tratan df
def addTasaDelitoPob(df, anyo, habitantes):
    aaaa = str(anyo)
    columnsTasaPob=df.columns[df.columns.str.contains(aaaa)]
    df['Delito/pob_'+ aaaa]=(df[columnsTasaPob[0]] / df[columnsTasaPob[1]]) * int(habitantes)

def calculateMediaDelitoPob(df,habitantes):

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