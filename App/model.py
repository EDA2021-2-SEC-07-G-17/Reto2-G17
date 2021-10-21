"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import newList
from DISClib.DataStructures.chaininghashtable import valueSet
import config as cf
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
import time
from time import process_time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'artworks': None,
               'medios': None,
               'artists': None,
               'Cids': None,
               'artistDate': None,
               'nacionalidad': None,
               'artistsMap': None,
               'artworksMap': None}

    catalog['artworks'] = lt.newList('SINGLE_LINKED', compareObjectIds)
    
    catalog['artworksMap'] = mp.newMap(numelements=147000,
                                    maptype='CHAINING',
                                    loadfactor=2.0,
                                    comparefunction=compareID)
    
    catalog['medios'] = mp.newMap(138112,
                                   maptype='CHAINING',
                                   loadfactor=2.0,
                                   comparefunction=compareMedium)

    catalog['artists'] = lt.newList('SINGLE_LINKED', compareConstituentsID)

    catalog['artistsMap'] = mp.newMap(numelements=16000,
                                    maptype="CHAINING",
                                    loadfactor=2.0,
                                    comparefunction=compareID)

    catalog['artistDate'] = mp.newMap(15300,
                                   maptype='CHAINING',
                                   loadfactor=2.0,
                                   comparefunction=compareyear)
    catalog['artworkDate'] = mp.newMap(15300,
                                   maptype='CHAINING',
                                   loadfactor=2.0,
                                   comparefunction=compareyear)                               

    catalog['nacionalidad'] = mp.newMap(100000, 
                                    maptype='CHAINING',
                                    loadfactor=1.0,
                                    comparefunction=compareyear)

    catalog['Cids'] = mp.newMap(15300,
                                   maptype='CHAINING',
                                   loadfactor=2.0,
                                   comparefunction=compareyear)
    return catalog



# Funciones para agregar informacion al catalogo

def AddArtworks(catalog, artwork):
    lt.addLast(catalog['artworks'], artwork)
    addnacionality(catalog, artwork)
    addlistyear2(catalog,artwork)

def AddArtworksMap(catalog, artworkm):
    mp.put(catalog['artworksMap'], artworkm['ObjectID'], artworkm)

def AddArtists(catalog, artist):
    lt.addLast(catalog['artists'],artist)
    addids(catalog,artist)
    addlistyear(catalog, artist)

def AddArtistsMap(catalog, artistm):
    mp.put(catalog['artistsMap'], artistm["DisplayName"], artistm)


def addlistmedium(catalog):
    medios = catalog["medios"]
    for art in lt.iterator(catalog["artworks"]):
        if mp.contains(medios, art["Medium"]):
            lista = mp.get(medios, art["Medium"])["value"]
            lt.addLast(lista, art)
            mp.put(medios, art["Medium"], lista)
        else:
            lst = lt.newList('ARRAY_LIST')
            lt.addLast(lst, art)
            mp.put(medios, art["Medium"], lst)
    return catalog


def addlistyear(catalog, artist):
    years = catalog["artistDate"]
    if mp.contains(years, artist["BeginDate"]):
        lista = mp.get(years, artist["BeginDate"])["value"]
        lt.addLast(lista, artist)
        mp.put(years, artist["BeginDate"], lista)
    else:
        lst = lt.newList('ARRAY_LIST')
        lt.addLast(lst, artist)
        mp.put(years, artist["BeginDate"], lst)
        
    return catalog
def addlistyear2(catalog, artwork):
    years = catalog["artworkDate"]
    date=artwork["DateAcquired"]
    datel=artwork["DateAcquired"].split('-')
    if datel[0]!="":
       dateacquired=date
    else:
       dateacquired="1-1-1"


    if mp.contains(years, dateacquired):
        lista = mp.get(years, dateacquired)["value"]
        lt.addLast(lista, artwork)
        mp.put(years, dateacquired, lista)
    else:
        lst = lt.newList('ARRAY_LIST')
        lt.addLast(lst, artwork)
        mp.put(years, dateacquired, lst)
    return catalog    


def addids(catalog, artist):
    mp.put(catalog["Cids"], artist["ConstituentID"], artist["DisplayName"])


def addnacionality(catalog, artwork):
    id = artwork["ConstituentID"]
    artistas = catalog["artists"]
    pos = id.replace('[','').replace(']','').replace(' ','').split(",")
    size = len(pos)
    i = 0
    j = 0
    if size > 1:
        nac = lt.newList("ARRAY_LIST")
        while j < size:
            for art in lt.iterator(artistas):
                if i < size and pos[i] == art["ConstituentID"]:
                    #if lt.isPresent(nac, art["Nationality"]) == 0:
                    lt.addLast(nac, art["Nationality"])
                    i += 1
            j += 1
        artwork["Nationality"] = nac
    else:
        nac = lt.newList("ARRAY_LIST")
        for art in lt.iterator(artistas):
            if pos[0] == art["ConstituentID"]:
                lt.addLast(nac, art["Nationality"])
        artwork["Nationality"] = nac

    return catalog


def nacionality(catalog):
    nac = catalog['nacionalidad']
    for art in lt.iterator(catalog["artworks"]):
        for nat in lt.iterator(art["Nationality"]):
            if mp.contains(nac, nat):
                lista = mp.get(nac, nat)['value']
                lt.addLast(lista, art)
                mp.put(nac, nat, lista)
            else:
                lista = lt.newList("ARRAY_LIST")
                lt.addLast(lista, art)
                mp.put(nac, nat, lista)            
    return catalog


# Funciones para creacion de datos

# Funciones de consulta


def cronartist(catalog, anio1, anio2):
    years = catalog["artistDate"]
    i = int(anio1)
    lista = lt.newList()
    while i <= anio2:
        i = str(i)
        if mp.contains(years, i):
            med = mp.get(years, i)["value"]
            for n in lt.iterator(med):
                lt.addLast(lista, n)
        i = int(i) + 1
    return lista

def id_artista(catalogo, artista):
    total_artistas = catalogo["artistsMap"]
    especifico = mp.get(total_artistas,artista)["value"]
    id_artista = especifico["ConstituentID"]
    return id_artista

def obras_artista(catalogo,artista):
    obras = mp.valueSet(catalogo["artworksMap"])
    lista = lt.newList(datastructure="ARRAY_LIST")

    for e in lt.iterator(obras):
        codigos = e["ConstituentID"]
        sub_codigos = codigos[1:int(len(lista)-1)]
        ncodigos = sub_codigos.split(", ")

        for h in ncodigos:
            if artista == h:
                lt.addLast(lista, e)
                break
                
    return lista

def medios_artista(catalogo, artista):
    id_especifico = id_artista(catalogo,artista)
    obras= obras_artista(catalogo,id_especifico)

    medios = mp.newMap(lt.size(obras)+10,
                        maptype='CHAINING',
                        loadfactor=2.0,
                        comparefunction=compareMedium)
    
    for o in lt.iterator(obras):
        if mp.contains(medios, o["Medium"]):
            lista = mp.get(medios, o["Medium"])['value']
            lt.addLast(lista, o)
            mp.put(medios, o["Medium"], lista)
        else:
            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, o)
            mp.put(medios, o["Medium"], lista)

    return medios

def req_3(catalogo,artista):
    id_artista_especifico = id_artista(catalogo,artista)
    obras = obras_artista(catalogo,id_artista_especifico)


    if obras:
        lista = lt.newList(datastructure="ARRAY_LIST")
        compareDates(obras)

        i = 1
        while i <= 3:
            x = lt.getElement(obras,i)
            lt.addLast(lista,x)
            i += 1
        
        j = 1
        while j <=3:
            x = lt.lastElement(obras)
            lt.addLast(lista, x)
            lt.removeLast(obras)
            j += 1

        return lista
    
    else:
        mensaje = "No se encontraron obras de ese autor"
        return mensaje


# Funciones utilizadas para comparar elementos dentro de una lista

def compareObjectIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareConstituentsID(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMedium(medio, entry):
    identry = me.getKey(entry)
    if (medio == str(identry)):
        return 0
    else:
        return -1

def compareID(medio, entry):
    identry = me.getKey(entry)
    if (medio == str(identry)):
        return 0
    else:
        return -1

def compareyear(medio, entry):
    identry = me.getKey(entry)
    if (medio == str(identry)):
        return 0
    else:
        return -1

def cronartist(catalog, anio1, anio2):
    years = catalog["artistDate"]
    i = int(anio1)
    lista = lt.newList("ARRAY_LIAT")
    while i <= anio2:
        i = str(i)
        if mp.contains(catalog["artistDate"], i):
            med = mp.get(years, i)["value"]
            for n in lt.iterator(med):
                lt.addLast(lista, n)
        i = int(i) + 1
    return lista

def cronartwork(catalog, fecha1,fecha2):
    years = catalog["artworkDate"]
    lista = lt.newList("ARRAY_LIST")
    new=mg.sort(mp.keySet(years), compareArtworkDate)
    for i in lt.iterator(new):
        if i>=fecha1 and i<=fecha2:
            if mp.contains(years,i):
               med = mp.get(years, i)["value"]
               for n in lt.iterator(med):
                   lt.addLast(lista, n)
    compras=getPurchase(lista)               
    return lista,compras

def getPurchase(lista):
    cont=0
    x=1
    while x <=lt.size(lista):
        if "purchase" in (lt.getElement(lista,x)["CreditLine"].lower()):
            cont+=1
        x+=1    
    return cont
    
def getNacion(catalogo):
    naciones=mp.keySet(catalogo["nacionalidad"])
    na=lt.newList("ARRAY_LIST")
    e=1
    n=0
    for i in lt.iterator(naciones):
        if i=="Nationality unknown" or i=="":
           n+=lt.size(lt.getElement(mp.valueSet(catalogo["nacionalidad"]),e)) 
        else:
           lt.addLast(na,{"pais":i,"num":lt.size(lt.getElement(mp.valueSet(catalogo["nacionalidad"]),e))})
        e+=1
    lt.addLast(na,{"pais":"Nationality unknown", "num":n})       
    new=mg.sort(na,sortnacion)
    mayores=lt.subList(new,1,10)
    mayor=mp.get(catalogo["nacionalidad"],lt.getElement(new,1)["pais"])["value"]
    primeras=getPrimeros(mayor)
    ultimas=getUltimos(mayor)
    
    return mayores,primeras,ultimas 
       


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDate(art1, art2):
    if art1['Date'] != '' and art2['Date'] != '':
        return float(art1['Date']) < float(art2['Date'])


def compareArtistDate(art1, art2):
    return float(art1) < float(art2)
def compareArtworkDate(art1, art2):
    return art1 < art2    

def elemento_mayor_mapa(medios):
    mayor = 0
    r = None
    for n in lt.iterator(mp.keySet(medios)):
        if lt.size(mp.get(medios, n)['value']) > mayor:
            mayor = lt.size(mp.get(medios, n)['value'])
            r = n
    return r

# Funciones de ordenamiento

def compareDates(mayor):
    mg.sort(mayor, compareDate)

def compareArtistsDates(catalog):
    years = catalog["artistDate"]
    med = mp.keySet(years)
    mg.sort(med, compareArtistDate)
def compareArworksDates(catalog):
    years = catalog["artworkDate"]
    med = mp.keySet(years)
    mg.sort(med, compareArtworkDate)    

 
def getUltimos(lista):
    posicionl=mp.size(lista)-2
    return lt.subList(lista, posicionl, 3)


def getPrimeros(lista):
    return lt.subList(lista, 1, 3)    
def sortnacion(pais1,pais2):
    
    return pais1["num"]>pais2["num"] 
        