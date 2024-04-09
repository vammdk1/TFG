import os


# Directorio donde se encuentran los archivos
directorio = 'OpCode'
# Lista para almacenar el contenido de los archivos
contenido_archivos = []
diccionario = []

# Obtener la ruta completa al directorio OpCode
directorio_padre = os.path.abspath(directorio)

# Obtener la lista de subdirectorios en el directorio OpCode
subdirectorios = [nombre for nombre in os.listdir(directorio_padre) if os.path.isdir(os.path.join(directorio_padre, nombre))]

# Iterar sobre los subdirectorios
for subdirectorio in subdirectorios:
    # Construir la ruta completa al subdirectorio
    ruta_subdirectorio = os.path.join(directorio_padre, subdirectorio)
    
    # Iterar sobre los archivos en el subdirectorio
    for nombre_archivo in os.listdir(ruta_subdirectorio):
        # Comprobar si el archivo es un archivo de texto
        if nombre_archivo.endswith('.txt'):
            # Construir la ruta completa al archivo
            ruta_archivo = os.path.join(ruta_subdirectorio, nombre_archivo)
            try:
                # Leer el contenido del archivo y almacenarlo en la lista
                with open(ruta_archivo, 'r') as archivo:
                    contenido = archivo.readline()
                    elementos = contenido.strip().split(":")
    
                    if len(elementos) > 1:
                        codigo = elementos[1].strip()
                        comandos = set(codigo.split())
                        contenido_archivos.extend(comandos)
            except Exception as e:
                print("Se produjo un error al leer el archivo:", e)

# Convertir el código de ensamblador en una matriz de valores numéricos
tempDicc = list(set(contenido_archivos))
diccionario = {instruccion: index for index, instruccion in enumerate(tempDicc, start=1)}

# Obtener la ruta del directorio padre de OpCode
directorio_padre_opcode = os.path.dirname(directorio_padre)

# Guardar el diccionario en un archivo de texto en el directorio padre de OpCode
ruta_diccionario = os.path.join(directorio_padre_opcode, 'diccionario.txt')
with open(ruta_diccionario, 'w') as archivo_salida:
    for instruccion, valor_numerico in diccionario.items():
        archivo_salida.write(f"{instruccion}: {valor_numerico}\n")

print("Diccionario guardado en:", ruta_diccionario)