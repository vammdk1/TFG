from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
import os
import subprocess
#librerías para los modelos
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
base_dir = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(base_dir, "upload")
DOWNLOAD_FOLDER = os.path.join(base_dir, "download")
DICTIONARY_FILE = os.path.join(base_dir, "imgGenerator", "diccionario.txt")
STATIC = os.path.join(base_dir, "webPage", "static")
MODELS_FOLDER = os.path.join(base_dir, "modelos")

last_message = None

# Lista de clases para predicción
classes = ['goodware', 'malware']

# Función para cargar la imagen
def cargar_imagen(ruta_imagen):
    img = image.load_img(ruta_imagen, target_size=(640, 460))  # Ajustar tamaño según tu modelo
    imagen_array = image.img_to_array(img)
    imagen_array = np.expand_dims(imagen_array, axis=0)
    return imagen_array

# Función para cargar todos los modelos
def cargar_modelos(modelos_dir):
    modelos_cargados = {}
    for archivo in os.listdir(modelos_dir):
        if archivo.endswith(".keras"):  # Filtrar solo archivos con extensión .keras
            ruta_modelo = os.path.join(modelos_dir, archivo)
            try:
                modelo_cargado = tf.keras.models.load_model(ruta_modelo)
                modelos_cargados[archivo] = modelo_cargado
            except Exception as e:
                print(f"Error cargando el modelo {archivo}: {e}")
    return modelos_cargados

# Cargar todos los modelos al inicio
modelos_cargados = cargar_modelos(MODELS_FOLDER)

@app.route('/webPage/static/<path:path>')
def send_static(path):
    return send_from_directory(STATIC, path)

@app.route("/")
def get_html():
    return render_template("mainPage.html")

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

    #procesar imagen
    procesar(file.filename)
    ruta_imagen = os.path.join(DOWNLOAD_FOLDER, "IMG.png")

    # Verifica si la imagen generada existe
    if not os.path.exists(ruta_imagen):
        return jsonify({"error": "Imagen no encontrada"}), 404

    # Cargar la imagen generada y hacer predicciones
    imagen_array = cargar_imagen(ruta_imagen)
    resultados = predecir_con_modelos(modelos_cargados, imagen_array)

    return jsonify(resultados)

 

def procesar(filename):
    script_file = os.path.join(base_dir, "imgGenerator", "imgTranslator.py")
    args = ["python", script_file, filename, DICTIONARY_FILE, UPLOAD_FOLDER, DOWNLOAD_FOLDER]
    subprocess.run(args)

def predecir_con_modelos(modelos_cargados, imagen_array):
    resultados = []
    for nombre_modelo, modelo in modelos_cargados.items():
        try:
            prediction = modelo.predict(imagen_array)
            clase_predicha = classes[np.argmax(prediction)]
            probabilidad_predicha = prediction[0][np.argmax(prediction)]
            resultados.append({
                "modelo": nombre_modelo,
                "clase_predicha": clase_predicha,
                "probabilidad_predicha": float(probabilidad_predicha)
            })
        except Exception as e:
            print(f"Error prediciendo con el modelo {nombre_modelo}: {e}")
    return resultados

@app.route("/download")
def download_img():
    filename = os.path.join(DOWNLOAD_FOLDER, "IMG.png")
    try:
        return send_from_directory(DOWNLOAD_FOLDER, "IMG.png", as_attachment=True)
    except FileNotFoundError:
        return {"error": "Imagen no encontrada"}

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/predictions", methods=["GET"])
def get_predictions():
       # Ruta de la imagen generada
    ruta_imagen = os.path.join(DOWNLOAD_FOLDER, "IMG.png")

    # Cargar la imagen generada y hacer predicciones
    imagen_array = cargar_imagen(ruta_imagen)
    resultados = predecir_con_modelos(modelos_cargados, imagen_array)

    return jsonify(resultados)