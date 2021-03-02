import csv

dataPath = 'src/data/'
fileName = '2016_1sc'
ext =".csv"
columnTitle = 2
sufProvincia ="Provincia de "
sufMunicipio="- Municipio de "
sufIsla = "- Isla de "
comunidad= "Comunidad"
provincia="Provincia"
municipio="Municipio"
code ="code"
printHead = False
newFile = []

with open(dataPath + fileName+ext, encoding='utf-8',newline='') as File:  
    reader = csv.reader(File)
    startData = False

    for row in reader:
        '''if i==10:
            break'''
        if len(row) > 0 and row[0].find(";") == 0 or startData:#columnas
            
            if not startData:
                startData = True
                columnsData = len(row[0].split(";"))

            data = row[0].split(";")

            if len(data) == columnTitle:
                if data[0].strip().find(sufProvincia) >=0:
                    provincia = data[0].strip()[len(sufProvincia):]
                elif data[0].strip().find(sufMunicipio) >=0:
                    municipio = data[0].strip()[len(sufMunicipio):]
                elif data[0].strip().find(sufIsla) >=0:
                    municipio = data[0].strip()[len(sufMunicipio):]
                else:
                    comunidad = data[0].strip()
                    provincia =""
                    municipio="" 


            elif len(data) == columnsData:
                
                #imprime cabecera
                if not data[0]:
                    dataaux = data[1:4]
                    dataaux.append("Delito")
                    dataaux += data[6:-1]
                    data = dataaux

                fila =[comunidad,provincia,municipio,code]+list(map(lambda x: x.strip(), data))

                withCode = fila[4].split(".-")
                if len(withCode) == 2:
                    fila[3] = withCode[0]
                    fila[4]= withCode[1]
                print(fila)
                newFile.append(fila)

with open(dataPath + fileName + "clean" +ext,'w', encoding='utf-8',newline = '') as result_file:
    wr = csv.writer(result_file, delimiter=";",quoting=csv.QUOTE_MINIMAL)
    wr.writerows(newFile, )
