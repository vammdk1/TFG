import os

# Directorio donde se encuentran los archivos
directorio = 'datos'
directorio_padre = os.path.dirname(directorio)

# Lista para almacenar el contenido de los archivos
contenido_archivos = []
diccionario = []


# Iterar sobre los archivos en el directorio
for nombre_archivo in os.listdir(directorio):
    # Comprobar si el archivo es un archivo de texto
    if nombre_archivo.endswith('.txt'):
        # Construir la ruta completa al archivo
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        try:
            # Leer el contenido del archivo y almacenarlo en la lista
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.readline()
                elementos = contenido.strip().split(":")

                if len(elementos)> 1 :
                    codigo = elementos[1].strip()
                    comandos = set(codigo.split())
                    contenido_archivos.extend(comandos)
        except Exception as e:
            print("Se produjo un error al leer el archivo:", e)

# Convertir el código de ensamblador en una matriz de valores numéricos
tempDicc = list(set(contenido_archivos))
diccionario = {instruccion: index for index, instruccion in enumerate(tempDicc, start=1)}

# Guardar el diccionario en un archivo de texto
ruta_diccionario = os.path.join(directorio_padre, 'diccionario.txt')
with open(ruta_diccionario, 'w') as archivo_salida:
    for instruccion, valor_numerico in diccionario.items():
        archivo_salida.write(f"{instruccion}: {valor_numerico}\n")

print("Diccionario guardado en:", ruta_diccionario)