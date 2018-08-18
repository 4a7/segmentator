#flask
from flask import Flask, render_template, request, send_from_directory, Response
import flask

#time
import time
import datetime

#pandas
import pandas as pd

#sistema
import sys
import os
from pathlib import Path

#keras
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.applications import vgg16, inception_v3, resnet50, mobilenet
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array



#secure_filename
from werkzeug.utils import secure_filename

#pil, numpy y matplotlib
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

DOWNLOAD_DIRECTORY="files"
app = Flask(__name__)

#inicializacion de modelos
vgg_model = None

def cargar_modelos():
    """Descripcion de la funcion cargar_modelos()
    Se encarga de cargar los modelos que se usaran para predecir imagenes
    """
    global vgg_model 
    vgg_model = vgg16.VGG16(weights='imagenet')
def preparar_imagen(image, target):
    """Descripcion de la funcion preparar_imagen()
    Se encarga de aplicarle preprocesamiento a la imagen para que se puede pasar al modelo
    """
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image
def modelo_predecir(img_path, model):
    """Descripcion de la funcion modelo_predecir()
    Se encarga de predecir la clase a la que pertenece el modelo
    """
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds
@app.route('/predictor', methods=['POST'])
def predictor():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = modelo_predecir(file_path, vgg_model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        result = str(pred_class[0][0][1])               # Convert to string
        return result
    return None
 
@app.route("/index")
@app.route("/")
def index():
    """Descripcion de la funcion index()
    Se encarga de devolver la pagina index.html renderizada
    Esta pagina tiene los links a los distintos elementos de la aplicacion
    Se llama desde la aplicacion web cuando se accede a /index o a /
    """
    return render_template("index.html")
@app.route("/cargar")
def cargar():
    """Descripcion de la funcion cargar()
    Se encarga de devolver la pagina cargar.html renderizada
    Esta pagina permite que un usuario cargue una imagen a la aplicacion
    Se llama desde la aplicacion web cuando se accede a /cargar
    """
    return render_template("cargar.html")
@app.route("/predecir")
def predecir():
    """Descripcion de la funcion predecir()
    Se encarga de devolver la pagina predecir.html renderizada
    Esta pagina le permite al usuario acceder a los algoritmos de keras
    Se llama desde la aplicacion web cuando se accede a /predecir
    """
    return render_template("predecir.html")    
@app.route("/generar")
def generar():
    """Descripcion de la funcion generar()
    Se encarga de devolver la pagina generar.html renderizada
    Esta pagina le permite a un usuario generar un archivo csv con pandas
    Se llama desde la aplicacion web cuando se accede a /generar
    """
    return render_template("generar.html") 
@app.route("/crear2")
def crear2():
    """Descripcion de la funcion crear()
    Se encarga de crear un archivo .csv y retornarlo
    Se llama mediante una peticion GET desde la pagina /generar
    """
    raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
        'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'], 
        'age': [42, 52, 36, 24, 73], 
        'preTestScore': [4, 24, 31, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70]}
    df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
    basepath = os.path.dirname(__file__)
    ts = time.time()
    st = str(datetime.datetime.fromtimestamp(ts).strftime('-%Y-%m-%d-%H-%M-%S'))
    nombre = "file"+st + ".csv"
    file_path = os.path.join(
            basepath, 'files', nombre)
    df.to_csv(file_path)
    nombre="files\\"+nombre
    print(42)
    print(nombre)
    #print(file_path)
    
    return "hello"#send_from_directory(nombre, as_attachment=True)
@app.route("/crear", methods = ['GET'])
def crear():
    """Descripcion de la funcion crear()
    Se encarga de crear un archivo .csv y retornarlo
    Se llama mediante una peticion GET desde la pagina /generar
    Parece tener un problema de cacheado de respuestas de GET
    """
    raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
        'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'], 
        'age': [42, 52, 36, 24, 73], 
        'preTestScore': [4, 24, 31, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70]}
    df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
    basepath = os.path.dirname(__file__)
    ts = time.time()
    st = str(datetime.datetime.fromtimestamp(ts).strftime('-%Y-%m-%d-%H-%M-%S'))
    nombre = "file"+st + ".csv"
    file_path = os.path.join(
            basepath, 'files', nombre)
    df.to_csv(file_path)
    print(nombre)
    #uploads = os.path.join(app.root_path, app.config['files'])
    return send_from_directory(directory=DOWNLOAD_DIRECTORY, filename=nombre, as_attachment=True)
    #return Response(df,mimetype='text/csv')

@app.route('/cargador', methods = ['GET', 'POST'])
def cargador():
    """Descripcion de la funcion cargador()
    Se encarga de cargar la imagen seleccionada por el usuario
    Realiza el procesamiento del nombre de la imagen para proteger contra eventos inesperados y colisiones de nombres
    Se llama mediante una peticion POST que envia la imagen
    """
    if request.method == 'POST':
        ts = time.time()
        st = str(datetime.datetime.fromtimestamp(ts).strftime('-%Y-%m-%d-%H-%M-%S'))
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        nombre=secure_filename(f.filename)
        nombre, extension = os.path.splitext(nombre)
        nombre = nombre + st + extension
        print(nombre)
        file_path = os.path.join(
            basepath, 'uploads', nombre)
        f.save(file_path)
        return render_template("exito.html", operacion = "Archivo cargado")
 
if __name__ == "__main__":
    print("Cargando modelos")
    cargar_modelos()
    print("Iniciando aplicacion")
    app.run(debug=False,threaded=False)