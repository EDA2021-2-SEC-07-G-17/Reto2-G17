import config as cf
import model
import csv
from time import process_time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de Obras.

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)
    start_time = process_time()
    loaddNacionality(catalog)
    stop_time = process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Tiempo de carga de las nacionalidades: " + str(elapsed_time_mseg))

    start = process_time()
    loadAddlistmedium(catalog)
    stop = process_time()
    elapsed_mseg = (stop - start)*1000
    print("Tiempo de carga de las técnicas: " + str(elapsed_mseg))


def loadArtworks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    artfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artfile, encoding='utf-8'))
    for obra in input_file:
        model.AddArtworks(catalog, obra)
        model.AddArtworksMap(catalog, obra)

def loadArtists(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    artfile = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artfile, encoding='utf-8'))
    for artist in input_file:
        model.AddArtists(catalog, artist)
        model.AddArtistsMap(catalog, artist)

def loaddNacionality(catalog):
    model.nacionality(catalog)

def loadAddlistmedium(catalog):
    model.addlistmedium(catalog)

# Funciones de ordenamiento

def compareDates(catalog, medio):
    model.compareDates(catalog, medio)
    return catalog

# Funciones de consulta sobre el catálogo

def cronartist(catalog, anio1, anio2):
    model.compareArtistsDates(catalog)
    retorno = model.cronartist(catalog, anio1, anio2)
    return retorno

def obras_tecnica(catalog, artista):
    lista = model.req_3(catalog, artista)
    return lista

def medios_artista(catalog, artista):
    mapa = model.medios_artista(catalog, artista)
    return mapa

def obras_artista(catalog, artista):
    id_especifico = model.id_artista(catalog, artista)
    lista  = model.obras_artista(catalog, id_especifico)
    return lista

def mayor_elemento(mapa):
    elemento = model.elemento_mayor_mapa(mapa)
    return elemento