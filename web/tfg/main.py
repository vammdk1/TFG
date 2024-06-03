from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import subprocess

app = Flask(__name__)
base_dir = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(base_dir, "upload")
DOWNLOAD_FOLDER = os.path.join(base_dir, "download")
DICTIONARY_FILE = os.path.join(base_dir, "imgGenerator", "diccionario.txt")
STATIC = os.path.join(base_dir, "webPage", "static")

last_message = None

@app.route('/webPage/static/<path:path>')
def send_static(path):
    return send_from_directory(STATIC, path)

@app.route("/")
def get_html():
    global last_message
    html_file = os.path.join(base_dir, "webPage", "mainPage.html")  # Construye la ruta relativa al archivo HTM
    
    if last_message:
        with open("webPage/mainPage.html", "r") as file:
            html_content = file.read()
            html_content = html_content.replace("{{last_message}}", last_message)
        return html_content, 200
    else:
        return send_file(html_file)

@app.route("/upload", methods=["POST"])
def upload_file():
    # Verifica si hay un archivo existente en la carpeta de upload
    existing_files = os.listdir(UPLOAD_FOLDER)
    if existing_files:
        # Elimina el archivo existente
        existing_file_path = os.path.join(UPLOAD_FOLDER, existing_files[0])
        os.remove(existing_file_path)

    # Asegúrate de que la carpeta de destino exista; si no, créala
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file = request.files["file"]
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    procesar(file.filename)
    return {"filename": file.filename, "status": "uploaded successfully"}

def procesar(filename):
    script_file = os.path.join(base_dir, "imgGenerator", "imgTranslator.py")
    args = ["python", script_file, filename, DICTIONARY_FILE, UPLOAD_FOLDER, DOWNLOAD_FOLDER]
    subprocess.run(args)

@app.route("/download")
def download_img():
    filename = os.path.join(DOWNLOAD_FOLDER, "IMG.png")
    try:
        return send_from_directory(DOWNLOAD_FOLDER, "IMG.png", as_attachment=True)
    except FileNotFoundError:
        return {"error": "Imagen no encontrada"}

if __name__ == "__main__":
    app.run(debug=True)
