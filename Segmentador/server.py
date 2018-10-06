import time
import datetime
import sys
import os

import hashlib
import flask
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from flask import Response, session, url_for, redirect
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads
from flask_uploads import IMAGES, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from pathlib import Path
from werkzeug.utils import secure_filename

from unet_CellSegmentation import *


DOWNLOAD_DIRECTORY = "files"
app = Flask(__name__)
dropzone = Dropzone(app)
servidor = 'mysql+pymysql://calidad:ss@localhost:3306/calidad_v1'
app.config['SQLALCHEMY_DATABASE_URI'] = servidor
db = SQLAlchemy(app)

# Se configura dropzone
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'exito'

# se configura uploads
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

# se configura la clave del api
app.config['SECRET_KEY'] = 'aire'
# app.secret_key = '22522837b0046ad6edf60333001ca426'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


@app.route("/index")
@app.route("/")
def index():
    """
    Se encarga de devolver la pagina index.html renderizada
    Esta pagina permite que las personas ingresen al sistema
    """
    # DEBUG: quitar estas lineas
    # session.pop('usuario', None)
    # session.pop('id_usuario', None)
    # session.pop('id_sesion', None)
    if 'usuario' in session:
        return render_template("index.html")
    return render_template("login.html")


@app.route("/i")
def i():
    session.pop('usuario', None)
    session.pop('id_usuario', None)
    session.pop('id_sesion', None)
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Se encarga de validar al usuario
    Se llama mediante una peticion POST que envia el usuario y la contrasena
    """
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        contrasena = hashlib.md5(contrasena.encode('utf-8')).hexdigest()
        data = db.session.query(modelos.Usuario).filter_by(
            correo=usuario, passwd=contrasena).first()
        # data = modelos.Usuario.query.filter_by(
        # correo=usuario, passwd=contrasena).first()
        if data is not None:    # login correcto
            nueva_sesion = modelos.Sesion()
            nueva_sesion.id_usuario = data.id_usuario
            db.session.add(nueva_sesion)
            db.session.commit()
            session['usuario'] = data.correo
            session['id_usuario'] = data.id_usuario
            session['id_sesion'] = nueva_sesion.id_sesion
            session['prefijo'] = 'sesion_'+str(nueva_sesion.id_sesion)
            print(session['prefijo'])
            return redirect(url_for('index'))
        else:
            session.pop('usuario', None)
            session.pop('id_usuario', None)
            session.pop('id_sesion', None)
            return render_template('login.html')
    else:
        return render_template("login.html")


@app.route('/visualizar')
def visualizar():
    """
    Muestra las imagenes cargadas en la sesion actual
    """
    id_sesion = session['id_sesion']
    file_urls = db.session.query(modelos.Archivo).join(
        modelos.SesionEntrada,
        modelos.SesionEntrada.id_archivo ==
        modelos.Archivo.id_archivo).filter(
            modelos.SesionEntrada.id_sesion ==
            id_sesion).all()
    print(file_urls)
    return render_template('visualizar.html', file_urls=file_urls)


@app.route('/segmentar')
def segmentar():
    """Se encarga de segmentar las imagenes
    """
    predict_web(session['dir_imagenes'],
                session['dir_imagenes_salida'], session['prefijo']+"_salida/")
    print(session['dir_imagenes'])
    return render_template('segmentar.html')


@app.route('/segmentar2')
def segmentar2():
    """Se encarga de segmentar las imagenes
    """
    # predict_web(session['dir_imagenes'], session['dir_imagenes_salida'],
    # session['prefijo']+"_salida/")
    return render_template('segmentar.html')


@app.route('/segmentadas')
def segmentadas():
    """
    Muestra las imagenes ya segmentadas
    """
    if "id_sesion" in session:
        id_sesion = session['id_sesion']
        file_urls = db.session.query(
            modelos.Archivo).join(modelos.SesionSalida,
                                  modelos.SesionSalida.id_archivo ==
                                  modelos.Archivo.id_archivo).filter(
                                      modelos.SesionSalida.id_sesion ==
                                      id_sesion).all()
        print(file_urls)
        return render_template('visualizar.html', file_urls=file_urls)
    else:   # en las pruebas, oara ver que funcione
        return render_template('index.html')


@app.route('/exito')
def exito():
    """Muestra un mensaje de exito cuando las imagenes se cargaron correctamente
    """
    return render_template('exito.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Descripcion de la funcion cargador()
    Se encarga de cargar la imagen seleccionada por el usuario
    Realiza el procesamiento del nombre de la imagen para proteger
    contra eventos inesperados y colisiones de nombres
    Se llama mediante una peticion POST que envia la imagen
    """
    if "file_urls" not in session:
        session['file_urls'] = []
    file_urls = session['file_urls']
    session['file_urls'] = []
    # file_urls=[]
    if request.method == 'POST':
        file_obj = request.files
        file_obj = request.files.getlist("file[]")
        print(file_obj)
        for f in file_obj:
            print(f)
            file = f
            ts = time.time()
            st = str(datetime.datetime.
                     fromtimestamp(ts).strftime('-%Y-%m-%d-%H-%M-%S'))
            nombre = secure_filename(file.filename)
            nombre, extension = os.path.splitext(nombre)
            nombre = nombre+st+extension
            filename = photos.save(
                file,
                name=nombre
            )
            file_urls.append(photos.url(filename))
        session['file_urls'] = file_urls
        return render_template("exito.html", file_urls=file_urls)


@app.route("/cargar")
def cargar():
    """
    Se encarga de devolver la pagina cargar.html renderizada
    Esta pagina permite que un usuario cargue una imagen a la aplicacion
    Se llama desde la aplicacion web cuando se accede a /cargar
    """
    return render_template("cargar.html")


@app.route('/cargador', methods=['GET', 'POST'])
def cargador():
    """
    Se encarga de cargar la imagen seleccionada por el usuario
    Realiza el procesamiento del nombre de la imagen
    para proteger contra eventos inesperados y colisiones de nombres
    Se llama mediante una peticion POST que envia la imagen
    """
    if "file_urls" not in session:
        session['file_urls'] = []
    file_urls = session['file_urls']
    # file_urls=[]
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            ts = time.time()
            # DEBUG: ponerle un timestamp a las fotos
            # st = str(datetime.datetime.fromtimestamp(ts).
            # strftime('-%Y-%m-%d-%H-%M-%S'))
            nombre = secure_filename(file.filename)
            nombre, extension = os.path.splitext(nombre)
            print(nombre)
            print(extension)
            nombre2 = os.getcwd() + '/uploads/' + session['prefijo'] + "/" + nombre + extension
            session['dir_imagenes'] = os.getcwd() + '/uploads/'+ session['prefijo']+"/"
            # se usara para la clasificacion
            session['dir_imagenes_salida'] = os.getcwd()+'/uploads/'+session['prefijo']+"_salida/"
            # se usara para almacenar los resutlados

            print(session['dir_imagenes_salida'])
            filename = photos.save(
                file,
                name=nombre2
            )
            filename = session['prefijo'] + "/" + nombre + extension
            # se obtiene el nombre para el url
            file_urls.append(photos.url(filename))
            nuevo_archivo = modelos.Archivo(nombre+extension,
                                            photos.url(filename))
            # nuevo_archivo.nombre = nombre+extension
            # nuevo_archivo.url = photos.url(filename)
            db.session.add(nuevo_archivo)
            db.session.commit()
            en_la_sesion = modelos.SesionEntrada()
            en_la_sesion.id_sesion = session['id_sesion']
            en_la_sesion.id_archivo = nuevo_archivo.id_archivo
            db.session.add(en_la_sesion)
            db.session.commit()
        session['file_urls'] = file_urls
        return "uploading..."


if __name__ == "__main__":
    print("Iniciando aplicacion")
    app.run(debug=False, threaded=False)
