from datetime import datetime
from sqlalchemy.sql import func
from hyperlink import _url

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
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_uploads import patch_request_class
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from pathlib import Path
from werkzeug.utils import secure_filename


"""
TODO
Mejorar la forma en la que se llama la segmentacion
Crear las tablas para resultados y mejorar la forma en la que se relacionan
Guardar el arreglo que se genera tras cada segmentacion en la carpeta
de resultados de la sesion
"""

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


class Usuario(db.Model):
    """
    Representacion de la tabla usuario
    """
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True)
    correo = db.Column(db.String(60))
    passwd = db.Column(db.String(32))


class Sesion(db.Model):
    """
    Representacion de la tabla sesion
    """
    id_sesion = db.Column('id_sesion', db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    fecha = db.Column(db.DateTime, nullable=True, default=func.now())
    usuario = db.relationship('Usuario',
                              backref=db.backref('usuario', lazy=True))


class Archivo(db.Model):
    """
    Representacion de la tabla archivo
    """
    id_archivo = db.Column('id_archivo', db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    url = db.Column(db.String(100))

    def __init__(self, nombre, url):
        self.nombre = nombre
        self.url = url


class SesionEntrada(db.Model):
    """
    Representacion de la tabla sesion_entrada
    """
    id_sesion = db.Column('id_sesion', db.Integer,
                          db.ForeignKey('sesion.id_sesion'), primary_key=True)
    id_archivo = db.Column(db.Integer, db.ForeignKey('archivo.id_archivo'),
                           primary_key=True)
    sesion = db.relationship('Sesion',
                             backref=db.backref('sesion', lazy=True))

    archivo = db.relationship('Archivo',
                              backref=db.backref('archivo', lazy=True))


class SesionSalida(db.Model):
    """
    Representacion de la tabla sesion_salida
    """
    id_sesion = db.Column('id_sesion', db.Integer,
                          db.ForeignKey('sesion.id_sesion'), primary_key=True)
    id_archivo = db.Column(db.Integer, db.ForeignKey('archivo.id_archivo'),
                           primary_key=True)
    tiempo_ejecucion = db.Column(db.Integer)
    precision = db.Column(db.Float)
    id_gt = db.Column(db.Integer, db.ForeignKey('archivo.id_archivo'))
    id_informe = db.Column(db.Integer, db.ForeignKey('archivo.id_archivo'))
    
    id_gt_rel = db.relationship("Archivo", foreign_keys=[id_gt])
    id_informe_rel = db.relationship("Archivo", foreign_keys=[id_informe])
    id_archivo_rel = db.relationship("Archivo", foreign_keys=[id_archivo])
    sesion = db.relationship('Sesion',
                             backref=db.backref('sesion2', lazy=True))
    #archivo = db.relationship('Archivo',
    #                          backref=db.backref('archivo2', lazy=True))
