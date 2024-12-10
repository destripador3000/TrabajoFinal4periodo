# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    id = db.Column(db.Integer, primary_key=True)
    libro = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), nullable=False)  # Aquí 'usuario' es el estudiante
    fecha = db.Column(db.Date, nullable=False)

    def __init__(self, libro, usuario, fecha):
        self.libro = libro
        self.usuario = usuario
        self.fecha = fecha

class Multa(db.Model):
    __tablename__ = 'multas'

    id = db.Column(db.Integer, primary_key=True)
    libro = db.Column(db.String(150), nullable=False)
    usuario = db.Column(db.String(150), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.Date)

    def __init__(self, libro, usuario,codigo, fecha_creacion):
        self.libro = libro
        self.usuario = usuario
        self.codigo=codigo
        self.fecha_creacion = fecha_creacion

class Libro(db.Model):
    __tablename__ = 'libro'
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada libro
    codigo = db.Column(db.String(100), unique=True, nullable=False)  # Código único del libro
    nombre = db.Column(db.String(200), nullable=False)  # Título del libro
    autor = db.Column(db.String(100), nullable=False)  # Autor del libro
    disponibilidad =db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Libro {self.codigo} - {self.nombre}>"

class Usuario(db.Model):
    __tablename__ = 'usuario'
    ID = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
   # rol=db.Column(db.String(100), nullable=True)
    
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # ID único para cada estudiante
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # Código único del estudiante
    nombre = db.Column(db.String(100), nullable=False)  # Nombre del estudiante

    def __repr__(self):
        return f"<Estudiante {self.codigo} - {self.nombre}>"