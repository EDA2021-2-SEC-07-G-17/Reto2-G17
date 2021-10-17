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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
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

    catalog['nacionalidad'] = mp.newMap(100000, 
                                    maptype='CHAINING',
                                    loadfactor=2.0,
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

def AddArtworksMap(catalog, artworkm):
    mp.put(catalog['artworksMap'], artworkm['ObjectID'], artworkm)

def AddArtists(catalog, artist):
    lt.addLast(catalog['artists'],artist)
    addids(catalog,artist)
    addlistyear(catalog, artist)

def AddArtistsMap(catalog, artistm):
    mp.put(catalog['artistsMap'], artistm["ConstituentID"], artistm)


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


def addids(catalog, artist):
    mp.put(catalog["Cids"], artist["ConstituentID"], artist["DisplayName"])


def addnacionality(catalog, artwork):
    id = artwork["ConstituentID"]
    artistas = catalog["artists"]
    pos = id.strip('[]').split(', ')
    size = len(pos)
    i = 0
    j = 0
    if size > 1:
        nac = lt.newList("ARRAY_LIST")
        while j < size:
            for art in lt.iterator(artistas):
                if i < size and pos[i] == art["ConstituentID"]:
                    if lt.isPresent(nac, art["Nationality"]) == 0:
                        lt.addLast(nac, art["Nationality"])
                    i += 1
            j += 1
        artwork["Nationality"] = nac
    else:
        for art in lt.iterator(artistas):
            nac = lt.newList("ARRAY_LIST")
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

def compareObjectIds(id1, id2):
    """
    Compara dos Objects ids de dos obras
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareConstituentsID(id1, id2):
    """
    Compara dos ConstituentID de dos obras
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMedium(medio, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
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
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (medio == str(identry)):
        return 0
    else:
        return -1

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


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDate(art1, art2):
    if art1['Date'] != '' and art2['Date'] != '':
        return float(art1['Date']) < float(art2['Date'])


def compareArtistDate(art1, art2):
    return float(art1) < float(art2)

# Funciones de ordenamiento


def compareDates(catalog, medio):
    medios = catalog["medios"]
    med = mp.get(medios, medio)["value"]
    mg.sort(med, compareDate)

def compareArtistsDates(catalog):
    years = catalog["artistDate"]
    med = mp.keySet(years)
    mg.sort(med, compareArtistDate)
