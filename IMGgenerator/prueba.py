import numpy as np
import cv2
import matplotlib.pyplot as plt

# Mandar archivo para revisar la lista
nombre_archivo = "IPv6addr.txt"

diccionario = {}

try:
    # Abrir el archivo en modo de lectura
    with open(nombre_archivo, 'r') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.readline()
        elementos =  contenido.strip().split(":")
        print("1")
        if len(elementos)> 1 :
            codigo = elementos[1].strip()
            comandos = set(codigo.split())

            # Convertir el código de ensamblador en una matriz de valores numéricos
            for index, instruccion in enumerate(comandos, start=1):
                diccionario[instruccion] = index

        print(diccionario)
        # Crear una lista de valores numéricos correspondientes a las instrucciones
        datos = [diccionario[instr] for instr in codigo.split()]

        # Crear una matriz cuadrada a partir de los datos
        lado_matriz = int(np.ceil(np.sqrt(len(datos))))
        matriz = np.zeros((lado_matriz, lado_matriz))

        # Llenar la matriz con los datos
        for i, val in enumerate(datos):
            fila = i // lado_matriz
            columna = i % lado_matriz
            matriz[fila, columna] = val

        # Aplicar la FFT a los datos
        fft_resultado = np.fft.fft2(matriz)

        # Calcular la magnitud del espectro de frecuencia
        magnitud_espectro = np.fft.fftshift(np.abs(fft_resultado))

        # Aplicar transformación logarítmica
        magnitud_log = np.log1p(magnitud_espectro)

        # Escalar linealmente los valores para ajustar el contraste
        magnitud_log_normalizada = cv2.normalize(magnitud_log, None, 0, 255, cv2.NORM_MINMAX)

        # Visualizar la magnitud logarítmica del espectro de frecuencia como una imagen
        plt.imshow(magnitud_log_normalizada, cmap='viridis')
        plt.colorbar()
        plt.title('Magnitud logarítmica del espectro de frecuencia')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Frecuencia (Hz)')
        plt.show()

except FileNotFoundError:
    print("El archivo especificado no se encontró.")
except Exception as e:
    print("Se produjo un error al leer el archivo:", e)

