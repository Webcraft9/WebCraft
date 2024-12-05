from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuración inicial de Flask
app = Flask(__name__)

# Configuración de la base de datos
USER_DB = 'root'
PASS_DB = 'root'
URL_DB = 'localhost'
NAME_DB = 'Qlocura'
FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy y Flask-Migrate
db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)

# Modelo de ejemplo: Person
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)

    def __init__(self, nombre, apellido, telefono, email, direccion, username, contrasena_hash, fecha_registro):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.username = username
        self.contrasena_hash = contrasena_hash
        self.fecha_registro = fecha_registro

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'username': self.username,
            'contrasena_hash': self.contrasena_hash,
            'fecha_registro': self.fecha_registro
        }

    def __str__(self):
        return f"{self.__class__.__name__}: {self.__dict__}"



