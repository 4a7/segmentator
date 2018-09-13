import time
import datetime
import sys
import os

from pathlib import Path
import flask
from flask import Flask, render_template, request, send_from_directory, Response, session, url_for, redirect
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from werkzeug.utils import secure_filename



DOWNLOAD_DIRECTORY="files"
app = Flask(__name__)
dropzone = Dropzone(app)

#Se configura dropzone
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'exito'

#se configura uploads
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

#se configura la clave del api
app.config['SECRET_KEY'] = 'aire'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

@app.route('/exito')
def exito():
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    return render_template('exito.html', file_urls=file_urls)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    """Descripcion de la funcion cargador()
    Se encarga de cargar la imagen seleccionada por el usuario
    Realiza el procesamiento del nombre de la imagen para proteger contra eventos inesperados y colisiones de nombres
    Se llama mediante una peticion POST que envia la imagen
    """
    if "file_urls" not in session:
        session['file_urls'] = []
    file_urls = session['file_urls']
    session['file_urls'] = []
    #file_urls=[]
    if request.method == 'POST':
        file_obj = request.files
        file_obj = request.files.getlist("file[]")
        print(file_obj)
        for f in file_obj:
            print(f)
            file = f
            ts = time.time()
            st = str(datetime.datetime.fromtimestamp(ts).strftime('-%Y-%m-%d-%H-%M-%S'))
            nombre = secure_filename(file.filename)
            nombre, extension = os.path.splitext(nombre)
            nombre = nombre+st+extension
            filename = photos.save(
                file,
                name = nombre    
            )
            file_urls.append(photos.url(filename))
        session['file_urls'] = file_urls        
        return render_template("exito.html", file_urls=file_urls)

@app.route("/index")
@app.route("/")
def index():
    """
    Se encarga de devolver la pagina index.html renderizada
    Esta pagina tiene los links a los distintos elementos de la aplicacion
    Se llama desde la aplicacion web cuando se accede a /index o a /
    """
    return render_template("index.html")

@app.route("/cargar")
def cargar():
    """
    Se encarga de devolver la pagina cargar.html renderizada
    Esta pagina permite que un usuario cargue una imagen a la aplicacion
    Se llama desde la aplicacion web cuando se accede a /cargar
    """
    return render_template("cargar.html")

@app.route('/cargador', methods = ['GET', 'POST'])
def cargador():
    """
    Se encarga de cargar la imagen seleccionada por el usuario
    Realiza el procesamiento del nombre de la imagen para proteger contra eventos inesperados y colisiones de nombres
    Se llama mediante una peticion POST que envia la imagen
    """
    if "file_urls" not in session:
        session['file_urls'] = []
    file_urls = session['file_urls']
    #file_urls=[]
    if request.method == 'POST':
        file_obj = request.files
        print(file_obj)
        for f in file_obj:
            file = request.files.get(f)
            ts = time.time()
            st = str(datetime.datetime.fromtimestamp(ts).strftime('-%Y-%m-%d-%H-%M-%S'))
            nombre = secure_filename(file.filename)
            nombre, extension = os.path.splitext(nombre)
            nombre = nombre + st + extension
            filename = photos.save(
                file,
                name = nombre    
            )
            file_urls.append(photos.url(filename))
        session['file_urls'] = file_urls        
        return "uploading..."

if __name__ == "__main__":
    print("Iniciando aplicacion")
    app.run(debug=False,threaded=False)