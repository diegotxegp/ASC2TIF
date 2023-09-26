import os
from osgeo import gdal
import rasterio
from pyproj import CRS
import time
from datetime import datetime

def convertir_asc_a_tif(archivo_asc, carpeta_gdb, epsg):

    carpeta_archivo_asc = os.path.basename(os.path.dirname(archivo_asc))
    archivo_tif = os.path.join(carpeta_gdb, carpeta_archivo_asc) + '.tif'

    if not os.path.exists(archivo_tif):
        try:
            driver = gdal.GetDriverByName('GTiff')
            ds = gdal.Open(archivo_asc)
            driver.CreateCopy(archivo_tif, ds)
            ds = None

            with rasterio.open(archivo_tif, 'r+') as f:
                    f.crs = CRS.from_epsg(epsg)

            print(f"Convertido: {archivo_asc} -> {archivo_tif}")
        except Exception as e:
            print(f"Error al convertir {archivo_asc} a TIFF: {str(e)}")


def convertir_asc_en_carpeta(carpeta, carpeta_gdb, epsg):

    for root, _, files in os.walk(carpeta):
        for archivo in files:
            if archivo.endswith(".asc"):
                carpeta_archivo_asc = os.path.basename(root)

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f"Inicio de {carpeta_archivo_asc}:", current_time)

                archivo_asc = os.path.join(root, archivo)
                convertir_asc_a_tif(archivo_asc, carpeta_gdb, epsg)

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f"Fin de {carpeta_archivo_asc}:", current_time)


if __name__ == '__main__':
    ########################################## MODIFICA AQUÍ ############################################################################
    carpeta_inicial = "P:\99_IMPACTOS COSTA\99_TEMPORAL\Diego\ASC_TIF"  # Reemplaza con la ruta de tu carpeta
    carpeta_gdb = "P:\99_IMPACTOS COSTA\99_TEMPORAL\Diego\ASC_TIF\Mapas_TIFF" # Reemplaza con la ruta de destino
    epsg = 3035  # EPSG
    tiempo_espera = 0 # horas
    #####################################################################################################################################
    
    # Temporizador para indicar cuántas horas después empezar
    print(f"El programa comenzará en {tiempo_espera} horas.")
    time.sleep(tiempo_espera*60*60)

    # Hora inicial del programa
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Inicio de programa: ", current_time)

    t_inicio = time.time()
    convertir_asc_en_carpeta(carpeta_inicial, carpeta_gdb, epsg)
    t_fin = time.time()
    
    # Hora final del programa
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Fin de programa: ", current_time)

    t_total = t_fin-t_inicio

    print(f"El programa tardó {t_total:.2f} segundos en ejecutarse.")