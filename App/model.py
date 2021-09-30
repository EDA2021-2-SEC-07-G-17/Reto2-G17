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
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newCatalog():
    catalog = {'artist': None,
               'artworks': None,
               'Medium': None}

    catalog['artist'] = lt.newList('SINGLE_LINKED')
    catalog['artworks'] = lt.newList('SINGLE_LINKED')
    catalog['Medium'] = mp.newMap(10000,
                                  maptype='CHAINING',
                                  loadfactor = 4.,
                                  comparefunction= CompareMediums)

    return catalog

def addArtWork(catalog, artwork):
    lt.addLast(catalog['artworks'],artwork)
    obra = mp.get(catalog['Medium'], artwork['Medium'])
    if obra:
        lt.addLast(me.getValue(obra),artwork)
    else:
        nuevasObras = lt.newList()
        mp.put(catalog['Medium'],artwork['Medium'],nuevasObras)



def addArtist(catalog, artist):
    lt.addLast(catalog['artist'],artist)

def addMedium(catalog, artwork):
    try:
        mediums = catalog['Medium']
        medium1 = artwork['Medium']
        existmedium = mp.contains(mediums, medium1)
        if existmedium:
            entry = mp.get(mediums, medium1)
            medium2 = me.getValue(entry)
        else:
            medium2 = newMedium(medium1)
            mp.put(mediums, medium1, medium2)
        lt.addLast(medium2['Medium'],artwork)
    except Exception:
        return None

def newMedium(medium):
    entry = {'Medium':"", 'artworks': None}
    entry['Medium'] = medium
    entry['artworks'] = lt.newList('SINGLE_LINKED', CompareMediums)
    return entry


# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta
def getOldestWorksByMedium(catalog, medium):
    mediums = mp.get(catalog['Medium'], medium)
    if mediums:
        return me.getValue(mediums)
    return None

# Funciones utilizadas para comparar elementos dentro de una lista
def CompareMediums(medium, entry):
    authentry = me.getKey(entry)
    if authentry == medium:
        return 0
    elif (medium > authentry):
        return 1
    else:
        return -1
# Funciones de ordenamiento
