# -*- coding: utf-8 -*-

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import numpy as np
import tensorflow as tf
from keras.preprocessing import image

base_dir = os.path.dirname(__file__)
modelo = os.path.join(base_dir,"modelos","modelo_Xception.keras")

print("Prueba de carga de modelo")
classes = ['goodware', 'malware']

# Cargar imagen
ruta_imagen = os.path.join('download', 'IMG.png')  # Ruta de la imagen a clasificar
imagen = image.load_img(ruta_imagen,target_size=(640, 460))  # Ajustar tamaño según tu modelo

# Convertir la imagen a un array numpy
imagen_array = image.img_to_array(imagen)

# Ajustar el formato del array
imagen_array = imagen_array.reshape((1,) + imagen_array.shape)

print( "Imagen cargada")

modelo_cargado = tf.keras.models.load_model(modelo)
prediction = modelo_cargado.predict(imagen_array)

# Interpretar la predicción
clase_predicha =  classes[np.argmax(prediction)]
probabilidad_predicha = prediction[0][np.argmax(prediction)]

print("Clase predicha:",clase_predicha)
print("Probabilidad predicha:", probabilidad_predicha)
