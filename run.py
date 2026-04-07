# run.py (En la raíz del proyecto, al mismo nivel que la carpeta 'app')

from app import create_app

# Creamos la instancia de la aplicación usando nuestra fábrica
app = create_app()

if __name__ == '__main__':
    # Arrancamos el servidor
    app.run(debug=True, host='0.0.0.0', port=5000)