from datetime import datetime
from sqlalchemy.sql import func
from server import *
from hyperlink import _url


class Usuario(db.Model):
    """
    Representacion de la tabla usuario
    """
    id_usuario = db.Column('id_usuario', db.Integer, primary_key = True)
    correo = db.Column(db.String(60))
    passwd = db.Column(db.String(32))
   
    
class Sesion(db.Model):
    """
    Representacion de la tabla sesion
    """
    id_sesion = db.Column('id_sesion', db.Integer, primary_key = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    fecha = db.Column(db.DateTime, nullable=True, default=func.now())
    usuario = db.relationship('Usuario',
        backref=db.backref('usuario', lazy=True))
    
class Archivo(db.Model):
    """
    Representacion de la tabla archivo
    """
    id_archivo = db.Column('id_archivo', db.Integer, primary_key = True)
    nombre = db.Column(db.String(45))
    url = db.Column(db.String(100))
    def __init__(self, nombre, url):
        self.nombre = nombre
        self.url = url

class SesionEntrada(db.Model):
    """
    Representacion de la tabla sesion_entrada
    """
    id_sesion = db.Column('id_sesion', db.Integer, db.ForeignKey('sesion.id_sesion'), primary_key = True)
    id_archivo = db.Column(db.Integer, db.ForeignKey('archivo.id_archivo'), primary_key = True)
    sesion = db.relationship('Sesion',
        backref=db.backref('sesion', lazy=True))
    archivo = db.relationship('Archivo',
        backref=db.backref('archivo', lazy=True))

class SesionSalida(db.Model):
    """
    Representacion de la tabla sesion_salida
    """
    id_sesion = db.Column('id_sesion', db.Integer, db.ForeignKey('sesion.id_sesion'), primary_key = True)
    id_archivo = db.Column(db.Integer, db.ForeignKey('archivo.id_archivo'), primary_key = True)
    tiempo_ejecucion = db.Column(db.Integer)
    precision = db.Column(db.Float)
    sesion = db.relationship('Sesion',
        backref=db.backref('sesion2', lazy=True))
    archivo = db.relationship('Archivo',
        backref=db.backref('archivo2', lazy=True))

 