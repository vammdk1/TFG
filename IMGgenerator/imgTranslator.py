import os
from matplotlib import pyplot as plt
import numpy as np


# Mandar archivos para revisar la lista
#TODO leer todos los archivos de OpCode

ruta_diccionario = 'diccionario.txt'
ruta_imagenes = 'img'
diccionario = {}


# Leer el diccionario desde el archivo
with open(ruta_diccionario, 'r') as archivo_diccionario:
    for linea in archivo_diccionario:
        # Dividir la línea en la instrucción y el valor numérico
        instruccion, valor_numerico = linea.strip().split(':')
        # Agregar la instrucción y el valor numérico al diccionario
        diccionario[instruccion.strip()] = int(valor_numerico.strip())
    #Sprint(diccionario)
        
# Longitud objetivo común
longitud_objetivo = 200000 

# Normalizar la longitud de las señales
def normalizar_longitud(datos, longitud_objetivo):
    if len(datos) > longitud_objetivo:
        # Truncar las señales más largas
        datos_normalizados = datos[:longitud_objetivo]
    else:
        # Calcular cuántas veces es necesario leer la señal para alcanzar el tamaño deseado
        veces_a_leer = int(np.ceil(longitud_objetivo / len(datos)))
        # Volver a leer los valores de la señal original
        datos_normalizados = np.tile(datos, veces_a_leer)[:longitud_objetivo]
        #datos_normalizados = np.pad(datos, (0, longitud_objetivo - len(datos)), mode='constant')
    return datos_normalizados

directorio_padre = os.path.abspath("OpCode")

# Obtener la lista de subdirectorios en el directorio OpCode
subdirectorios = [nombre for nombre in os.listdir(directorio_padre) if os.path.isdir(os.path.join(directorio_padre, nombre))]

# Iterar sobre los subdirectorios
for subdirectorio in subdirectorios:
    # Construir la ruta completa al subdirectorio
    ruta_subdirectorio = os.path.join(directorio_padre, subdirectorio)
    # Iterar sobre los archivos en el subdirectorio
    for nombre_archivo in os.listdir(ruta_subdirectorio):
        ruta_archivo = os.path.join(ruta_subdirectorio, nombre_archivo)
        try:
            # Abrir el archivo en modo de lectura
            with open(ruta_archivo, 'r') as archivo:
                # Leer el contenido del archivo
                contenido = archivo.readline()
                elementos =  contenido.strip().split(":")
                if len(elementos)> 1 :
                    codigo = elementos[1].strip()
                    
                    # Asignar a los strings en codigo sus respectivos valores del diccionario
                    codigo_con_valores = [diccionario.get(c, 0) for c in codigo.split()]
                    #print(codigo_con_valores)

                    # Normalizar la longitud de los datos
                    datos_normalizados = normalizar_longitud(np.array(codigo_con_valores, dtype=float), longitud_objetivo)
                    # Aplicar la FFT a los datos
                    fft_resultado = np.fft.fft(datos_normalizados)

                    frecuencia_muestreo = 1

                    # Calcular el espectrograma
                    espectrograma = plt.specgram(fft_resultado, Fs=frecuencia_muestreo, cmap='viridis')

                    valor_minimo_colorbar = 0  # Valor mínimo deseado en la barra de color (dB)
                    valor_maximo_colorbar = 100   # Valor máximo deseado en la barra de color (dB)
                    espectrograma[3].set_clim(valor_minimo_colorbar, valor_maximo_colorbar)
                    # Ocultar los números en los ejes x e y
                    plt.colorbar().remove()
                    plt.xticks([])
                    plt.yticks([])
                    #eliminar el margen
                    plt.tight_layout(pad=0)
                    
                    

                    # Guardar el espectrograma en un archivo de imagen
                    ruta_archivo = ruta_archivo.split("\\")
                    carpeta = ruta_archivo[len(ruta_archivo)-2]
                    nombre_archivo = ruta_archivo[len(ruta_archivo)-1].split(".")[0]

                    if not os.path.exists('img'):
                        os.makedirs('img')
                    if not os.path.exists('img/'+carpeta):
                        os.makedirs('img/'+carpeta)

                    plt.savefig('img/'+carpeta+'/'+nombre_archivo+'_imagen.png')
                    #plt.show()
                    plt.clf()
        except FileNotFoundError:
            print("El archivo especificado no se encontró.")
        except Exception as e:
            print("Se produjo un error al leer el archivo:", e)