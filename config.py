import os

# Directorio base de la aplicación
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # URI de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'biblioteca.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Clave secreta para sesiones y CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    # Otros valores de configuración
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() in ['true', '1', 'yes']
