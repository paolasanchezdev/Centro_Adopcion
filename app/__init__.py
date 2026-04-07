# app/__init__.py

from flask import Flask

def create_app():
    # Inicializamos Flask. Al estar en la carpeta 'app', buscará templates y static aquí adentro automáticamente.
    app = Flask(__name__)

    # Importamos y registramos nuestro Blueprint de rutas
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app