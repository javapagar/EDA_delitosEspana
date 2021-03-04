import csv

listaAnyos = ['2016','2017','2018','2019','2020']

dataPath = 'src/data/'
fileName = ''
ext =".csv"
columnTitle = 2
sufProvincia ="Provincia de "
sufMunicipio="- Municipio de "
sufIsla = "- Isla de "
code ="code"


for anyo in listaAnyos:
    for i in range(1,5):
        comunidad= "Comunidad"
        provincia="Provincia"
        municipio="Municipio"
        newFile = []
        fileName = anyo + "_"+str(i)+"sc"
        with open(dataPath + fileName + ext, encoding='utf-8',newline='') as File:  
            #reader = csv.reader(File)
            startData = False

            for row in File:
                '''if i==10:
                    break'''
                if len(row) > 0 and row.find(";") == 0 or startData:#columnas
                    
                    if not startData:
                        startData = True
                        columnsData = len(row.split(";"))

                    data = row.split(";")

                    if len(data) == columnTitle:
                        if data[0].strip().find(sufProvincia) >=0:
                            provincia = data[0].strip()[len(sufProvincia):]
                            nivel = "Provincia"
                        elif data[0].strip().find(sufMunicipio) >=0:
                            municipio = data[0].strip()[len(sufMunicipio):]
                            nivel = "Municipio"
                        elif data[0].strip().find(sufIsla) >=0:
                            municipio = data[0].strip()[len(sufMunicipio):]
                            nivel = "Municipio"
                        else:
                            comunidad = data[0].strip()
                            provincia =""
                            municipio="" 
                            nivel = "Comunidad"


                    elif len(data) == columnsData:
                        
                        #imprime cabecera
                        if not data[0]:
                            data[0]="Delito"
                            data[-1]="Nivel"
                        else:
                            data[-1] = nivel

                        fila =[comunidad,provincia,municipio,code]+list(map(lambda x: x.strip(), data))
                        

                        withCode = fila[4].split(".-")
                        if len(withCode) == 2:
                            fila[3] = withCode[0]
                            fila[4]= withCode[1]
                        print(fila)
                        newFile.append(fila)

        with open(dataPath + fileName + "clean" + ext,'w', encoding='utf-8',newline = '') as result_file:
            wr = csv.writer(result_file, delimiter=";",quoting=csv.QUOTE_MINIMAL)
            wr.writerows(newFile, )
        