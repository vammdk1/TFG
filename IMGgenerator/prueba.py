from matplotlib import pyplot as plt
import numpy as np
import cv2
import os

#TODO cambiar a espectograma   

# Mandar archivos para revisar la lista
nombres_archivos = ["OpCode/goodware/IPv6addr.txt", "OpCode/goodware/vstp.txt", "OpCode/goodware/tickle_tcp.txt"]
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
    print(diccionario)

for nombre_archivo in nombres_archivos:
    try:
        # Abrir el archivo en modo de lectura
        with open(nombre_archivo, 'r') as archivo:
            # Leer el contenido del archivo
            contenido = archivo.readline()
            elementos =  contenido.strip().split(":")
            if len(elementos)> 1 :
                codigo = elementos[1].strip()
                
                # Asignar a los strings en codigo sus respectivos valores del diccionario
                codigo_con_valores = [str(diccionario.get(c, 0)) for c in codigo.split()]
                print(codigo_con_valores)
                # Convertir los datos a un array de tipo float
                datos = np.array(codigo_con_valores, dtype=float)

                # Aplicar la FFT a los datos
                fft_resultado = np.fft.fft(datos)

                # Calcular la magnitud del espectro de frecuencia
                magnitud_espectro = np.abs(fft_resultado)

                # Aplicar transformación logarítmica
                magnitud_log = np.log1p(magnitud_espectro)
                # Calcular el espectrograma del espectro de frecuencia
                plt.clf()
                plt.specgram(magnitud_log, cmap='hot')
                plt.colorbar()
                plt.title('Espectrograma del espectro de frecuencia')
                plt.xlabel('Tiempo')
                nombre_archivo = nombre_archivo.split("/")
                nombre_archivo = nombre_archivo[2]
                nombre_archivo = nombre_archivo.split(".")
                nombre_archivo = nombre_archivo[0]
                plt.savefig('img/'+nombre_archivo+'_imagen.png')
                #plt.show()

    except FileNotFoundError:
        print("El archivo especificado no se encontró.")
    except Exception as e:
        print("Se produjo un error al leer el archivo:", e)


