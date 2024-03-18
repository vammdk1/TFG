from matplotlib import pyplot as plt
import numpy as np

#TODO cambiar a espectograma   

# Mandar archivos para revisar la lista
nombres_archivos = ["OpCode/malware/0a65d76177f165424a529f35c2ec4a5d.txt", "OpCode/malware/0c49f4b9c1357bbf92b3a0b2430ab49f.txt",
                     "OpCode/malware/0d2295388bd65c7ae77fa115f827bf14.txt", "OpCode/goodware/IPv6addr.txt", "OpCode/goodware/vstp.txt", "OpCode/goodware/tickle_tcp.txt"]
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
longitud_objetivo = 20000  # Por ejemplo, la longitud más corta entre todas las señales

# Normalizar la longitud de las señales
def normalizar_longitud(datos, longitud_objetivo):
    if len(datos) > longitud_objetivo:
        # Truncar las señales más largas
        datos_normalizados = datos[:longitud_objetivo]
    else:
        # Rellenar las señales más cortas con ceros
        # Calcular cuántas veces es necesario leer la señal para alcanzar el tamaño deseado
        veces_a_leer = int(np.ceil(longitud_objetivo / len(datos)))
        # Volver a leer los valores de la señal original
        datos_normalizados = np.tile(datos, veces_a_leer)[:longitud_objetivo]
        #datos_normalizados = np.pad(datos, (0, longitud_objetivo - len(datos)), mode='constant')
    return datos_normalizados

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
                codigo_con_valores = [diccionario.get(c, 0) for c in codigo.split()]
                #print(codigo_con_valores)

                # Normalizar la longitud de los datos
                datos_normalizados = normalizar_longitud(np.array(codigo_con_valores, dtype=float), longitud_objetivo)

                # Convertir los datos a un array de tipo float
                #datos = np.array(datos_normalizados, dtype=float)

                print(len(datos_normalizados))

                # Aplicar la FFT a los datos
                fft_resultado = np.fft.fft(datos_normalizados)

                frecuencia_muestreo = 1

                # Calcular el espectrograma
                espectrograma = plt.specgram(fft_resultado, Fs=frecuencia_muestreo, cmap='viridis')

                # Mostrar el espectrograma
                
                plt.xlabel('Tiempo [s]')
                plt.ylabel('Frecuencia [Hz]')
                plt.title('Espectrograma')
                plt.colorbar(mappable=espectrograma[3]) 
                nombre_archivo = nombre_archivo.split("/")
                nombre_archivo = nombre_archivo[2]
                nombre_archivo = nombre_archivo.split(".")
                nombre_archivo = nombre_archivo[0]
                plt.savefig('img/'+nombre_archivo+'_imagen.png')
                #plt.show()
                plt.clf()

    except FileNotFoundError:
        print("El archivo especificado no se encontró.")
    except Exception as e:
        print("Se produjo un error al leer el archivo:", e)


