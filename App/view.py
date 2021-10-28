"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """



import config as cf
import sys
import controller
from time import process_time
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


# FUNCIONES PARA LA IMPRESIÓN DE RESULTADOS        

def artworksporpais(retorno):
    print("\nLos diez paises con mas obras son: " )
    for i in lt.iterator(retorno[0]):
        print(i["pais"]+":  "+str(i["num"]))
    print("Muestra de las obras del pais con mas de ellas: "+str(lt.getElement(retorno[0],1)["pais"]))    
    nw = retorno[1]
    nw2=retorno[2]
    for x in lt.iterator(nw):
            print("\n Titulo: " + x["Title"] + "\n Artista(s): " + x["ConstituentID"] + 
                "\n Fecha: " + x["DateAcquired"] + "\n Medio: " + x["Medium"]
                + "\n Dimensiones: " + x["Dimensions"] + "\n")
    for x in lt.iterator(nw2):
            print("\n Titulo: " + x["Title"] + "\n Artista(s): " + x["ConstituentID"] + 
                "\n Fecha: " + x["DateAcquired"] + "\n Medio: " + x["Medium"]
                + "\n Dimensiones: " + x["Dimensions"] + "\n")

def rangoartworks(retorno, anio1, anio2):
    size = lt.size(retorno)
    print("\nLa cantidad de obras de arte adquiridas entre " + str(anio1) + " y "
        + str(anio2) + " es: " + str(size))
    print("Muestra de las obras adquiridas en este rango: ")
    if size:
        i = 1
        nw = lt.newList()
        while i <= 3:
            lt.addLast(nw, lt.getElement(retorno, i))
            i += 1
        i = size - 2
        while i <= size:
            lt.addLast(nw, lt.getElement(retorno, i))
            i += 1
        for x in lt.iterator(nw):
            print("\n Titulo: " + x["Title"] + "\n Artista(s): " + x["ConstituentID"] + 
                "\n Fecha: " + x["DateAcquired"] + "\n Medio: " + x["Medium"]
                + "\n Dimensiones: " + x["Dimensions"] + "\n")
    else:
        print("No se encontraron obras en este rango de fechas")

# MENU

def printMenu():
    print("\nBienvenido")
    print("1- Inicializar el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Buscar a los autores nacidos en un rango de años->Req 1")
    print("4- Contar el número total de obras en un rango de fechas determinado->Req 2")
    print("5- Clasificar las obras de un artista por técnica->Req 3")
    print("6- Contar el número total de obras por paises->Req 4")
    print("7- Costo de transportar las obras de un departamento->Req 5")
    print("Lab 6 \n8- Contar el número total de obras de una Nacionalidad")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)
        print("\nTotal obras Cargadas: " + str(lt.size(catalog["artworks"])))
        print("Total obras en mapa: " + str(mp.size(catalog["artworksMap"])))
        print("Total artistas Cargados: " + str(lt.size(catalog["artists"])))
        print("Total artistas en mapa: " + str(mp.size(catalog["artistsMap"])))
        print("Total años Cargados: " + str(mp.size(catalog["artistDate"])))
        print("Total técnicas Cargadas: " + str(mp.size(catalog["medios"])))
        print("Total C ids caragados: " + str(mp.size(catalog["Cids"])))
        print("Total Nacionalidades cargadas: " + str(mp.size(catalog["nacionalidad"])))

    elif int(inputs[0]) == 3:
        tiempo_inicio=time.process_time()
        inicial = int(input("Ingrese el año inicial a consultar: \n"))
        final = int(input("Ingrese el año final a consultar: \n"))
        inicial = int(input("Ingrese el año inicial a consultar: "))
        final = int(input("Ingrese el año final a consultar: "))
        resultado  = controller.cronartist(catalog, inicial, final)
        tamaño = lt.size(resultado)
        print("\nLa cantidad de artistas que nacieron entre " + str(inicial) + " y "
        + str(final) + " es: " + str(tamaño))
        print("Muestra de los artistas nacidos en este rango: ")
        if tamaño:
            i = 1
            nw = lt.newList()
            while i <= 3:
                lt.addLast(nw, lt.getElement(resultado, i))
                i += 1
            i = tamaño - 2
            while i <= tamaño:
                lt.addLast(nw, lt.getElement(resultado, i))
                i += 1
            for x in lt.iterator(nw):
                print("\n Nombre: " + x["DisplayName"] + "\n Año de Nacimiento: " + x["BeginDate"] + 
                    "\n Año de Fallecimiento: " + x["EndDate"] + "\n Nacionalidad: " + x["Nationality"]
                    + "\n Género: " + x["Gender"] + "\n Bio: " + x["ArtistBio"]+ "\n Wiki QID: " + x["Wiki QID"]
                    + "\n ULAN: " + x["ULAN"])
        else:
            print("No se encontraron artistas en este rango de fechas")
        tiempo_fin=time.process_time()
        TimeMseg=(tiempo_fin-tiempo_inicio)*1000
        print (TimeMseg)    

    elif int(inputs[0]) == 4:
        tiempo_inicio=time.process_time()
        inicial = input("Ingrese la fecha inicial a consultar: \n")
        final = input("Ingrese la fecha final a consultar: \n")
        inicial = input("Ingrese la fecha inicial a consultar: ")
        final = input("Ingrese la fecha final a consultar: ")
        resultado  = controller.cronartwork(catalog, inicial, final)
        rangoartworks(resultado[0], inicial, final)
        print("Y el total de obras compradas es de: "+str(resultado[1]))
        tiempo_fin=time.process_time()
        TimeMseg=(tiempo_fin-tiempo_inicio)*1000
        print (TimeMseg)

    elif int(inputs[0]) == 5:
        tiempo_inicio=time.process_time()
        nombre = str(input("Escriba el nombre del artista: "))
        lista = controller.obras_tecnica(catalog, nombre)
        
        medios = controller.medios_artista(catalog, nombre)
        tamaño = mp.size(medios)
        
        obras = lt.size(controller.obras_artista(catalog, nombre))

        mayor = controller.mayor_elemento(medios)

        print("El artista "+str(nombre)+" tiene "+str(obras)+" en el museo")
        print("Esas obras usan "+str(tamaño)+" tecnicas")
        print("El medio o tecnica más usado por este artista es: "+str(mayor))

        for art in lt.iterator(lista):
            print('\nObjectID: ' + art["ObjectID"] + '\nTítulo: ' + art["Title"] + '\nFecha de la obra: ' + art["Date"] + 
                    '\nTécnica: ' + art["Medium"] + '\nDimensiones: ' + art["Dimensions"] + '\nFecha de adquisición: ' + art["DateAcquired"]
                    +'\nDepartamento: ' + art["Department"] + '\nClasificación: ' + art["Classification"]+ '\nURL: ' + art["URL"])
        tiempo_fin=time.process_time()
        TimeMseg=(tiempo_fin-tiempo_inicio)*1000
        print (TimeMseg)
    elif int(inputs[0])==6:
        tiempo_inicio=time.process_time()
        resultado=controller.getNacion(catalog)
        artworksporpais(resultado)
        tiempo_fin=time.process_time()
        TimeMseg=(tiempo_fin-tiempo_inicio)*1000
        print (TimeMseg)    
        
    elif int(inputs[0])==7:
        departamento = input("Escriba el nombre del departamento del cual quiera saber su costo de transporte: ")
        start_time = process_time()
        departamentos_total = catalog['departamento']
        n_obras_departamento = lt.size(mp.get(departamentos_total,departamento)["value"])
        mapa_total = controller.costos_transporte(catalog,departamento)
        peso = mp.get(mapa_total, "peso")['value']
        precio = mp.get(mapa_total, "precio")['value']
        costosas = mp.get(mapa_total, "costosas")['value']
        antiguas = mp.get(mapa_total, "antiguas")['value']

        if n_obras_departamento:
            print("El museo debe transportar "+str(n_obras_departamento)+" del departamento de "+str(departamento))
            print("El precio estimado del transporte es de "+str(precio)+" USD")
            print("El peso estimado de todas las obras del departamento es de: "+str(peso)+" Kg")
            print("Las 5 obras mas antiguas a transportar son:")

            for e in lt.iterator(antiguas):
                print("\nTitulo: " + e["Title"] + "\nAutores: " + e["ConstituentID"] + 
                        "\nClasificación: " + e["Classification"] + "\nFecha: " + e["Date"] +
                        "\nTécnica: " + e["Medium"] + "\nDimensiones: " + e["Dimensions"] + "\nCosto de transporte: " + str(e["transporte"]))

            print("Las 5 obras mas costosas de transportar son: ")

            for i in lt.iterator(costosas):
                print("\nTitulo: " + i["Title"] + "\nAutores: " + i["ConstituentID"] + 
                        "\nClasificación: " + i["Classification"] + "\nFecha: " + i["Date"] +
                        "\nTécnica: " + i["Medium"] + "\nDimensiones: " + i["Dimensions"] + "\nCosto de transporte: " + str(i["transporte"]))
        
        stop_time = process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(str(elapsed_time_mseg))


    
    elif int(inputs[0]) == 8:
        """
        Esto es del Laboratorio 6
        """
        tiempo_inicio=time.process_time()
        nacionalidad = input("Ingrese la nacionalidad a consultar: \n")
        nacionalidad = input("Ingrese la nacionalidad a consultar: ")
        if mp.contains(catalog["nacionalidad"], nacionalidad):
            total = mp.get(catalog["nacionalidad"], nacionalidad)['value']
            size = lt.size(total)
            print("La cantidad de obras de la nacionalidad " + nacionalidad + 
                    ": " + str(size))
        else:
            print("No se encontró dicha nacionalidad")
        tiempo_fin=time.process_time()
        TimeMseg=(tiempo_fin-tiempo_inicio)*1000
        print (TimeMseg)    
        
    else:
        print("Cerrando aplicación... ")
        sys.exit(0)
sys.exit(0)
