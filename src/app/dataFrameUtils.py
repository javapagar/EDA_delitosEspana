
def getQColumns(df):
    return df.columns[df.columns.str.contains('Q')]

def getNacional(df):
    return df[df.Comunidad.str.contains('NACIONAL') & df.Delito.str.contains('TOTAL')]