import sys
from matplotlib import pyplot as plt
import numpy as np


# Mandar archivos para revisar la lista
#TODO leer todos los archivos de OpCode

ruta_diccionario = 'diccionario.txt'
ruta_lectura = '/home/victor/tfg/upload'
ruta_guardado = '/home/victor/tfg/download'
diccionario = {}

elementos = sys.argv
# Leer el diccionario desde el archivo
with open(elementos[2], 'r') as archivo_diccionario:
    for linea in archivo_diccionario:
        # Dividir la línea en la instrucción y el valor numérico
        instruccion, valor_numerico = linea.strip().split(':')
        # Agregar la instrucción y el valor numérico al diccionario
        diccionario[instruccion.strip()] = int(valor_numerico.strip())
    #Sprint(diccionario)
        
# Longitud objetivo común
longitud_objetivo = 20000 

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

# Obtener la lista de subdirectorios en el directorio OpCode
try:
    print(ruta_lectura)
    # Abrir el archivo en modo de lectura
    with open(ruta_lectura+"/"+elementos[1], 'r') as archivo:
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

            print("Guardado en :"+ruta_guardado+'/IMG.png')
            plt.savefig(ruta_guardado+'/IMG.png')
            #plt.show()
            plt.clf()
except FileNotFoundError:
    print("El archivo especificado no se encontró.")
except Exception as e:
    print("Se produjo un error al leer el archivo:", e)