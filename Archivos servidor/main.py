from click import File
import os
from fastapi import FastAPI, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura la ruta para servir archivos estáticos desde tu directorio "extras"
app.mount("/static", StaticFiles(directory="webPage/static",html=True), name="static")

@app.get("/")
async def get_html():
     return FileResponse("webPage/mainPage.html")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Define la ruta de destino donde se guardarán los archivos
    upload_folder = "/home/victor/tfg/upload/"

    # Verifica si hay un archivo existente en la carpeta de upload
    existing_files = os.listdir(upload_folder)
    if existing_files:
        # Elimina el archivo existente
        existing_file_path = os.path.join(upload_folder, existing_files[0])
        os.remove(existing_file_path)
        
    # Asegúrate de que la carpeta de destino exista; si no, créala
    os.makedirs(upload_folder, exist_ok=True)
    # Concatena el nombre del archivo con la ruta de la carpeta de destino
    file_path = os.path.join(upload_folder, file.filename)
    # Guarda el archivo en la ubicación especificada
    with open(file_path, "wb") as f:
        f.write(await file.read())

    procesar(file.filename)
    
    # Enviar una respuesta al cliente
    return {"filename": file.filename, "status": "uploaded successfully"}

def procesar (filename):
    print("procesando")
    script = "/home/victor/tfg/imgGenerator/imgTranslator.py"
    diccionario = "/home/victor/tfg/imgGenerator/diccionario.txt"
    args= [script, filename,diccionario ]
    print(script)
    subprocess.run(["python3"] + args)
    



@app.get("/download")
async def download_img():
    #ruta del objeto
    download_folder ="/home/victor/tfg/download/IMG.png"

    try:
        #leer imagen
        with open(download_folder, "rb") as file:
            img_content = file.read()

        #respuesta http
        response = Response(content = img_content, media_type="image/jpeg")
        response.headers["Content-Disposition"] = f"attachment; filename=image.jpg"

        return response
    except FileNotFoundError:
        return {"error":"Imagen no encontrada"}