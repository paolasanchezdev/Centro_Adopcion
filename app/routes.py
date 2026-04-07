from flask import Blueprint, render_template, request, redirect, url_for, flash
import app.database as database
from .models import Dog

# Creamos el Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Catálogo principal de perritos disponibles"""
    dogs_data = database.get_available_dogs()
    # Mapeo de datos a objetos Dog (id, name, breed, age, image_url)
    available_dogs = [Dog(row[0], row[1], row[2], row[3], row[4]) for row in dogs_data]
    return render_template('catalogo.html', dogs=available_dogs)

@main_bp.route('/adoptar/<int:dog_id>')
def form_adopcion(dog_id):
    """Formulario de confirmación con la foto del perro"""
    dog = database.get_dog_by_id(dog_id)
    if not dog:
        return "Perrito no encontrado", 404
    
    # Creamos el objeto para usar dog.image_url en el HTML
    dog_obj = Dog(dog[0], dog[1], dog[2], dog[3], dog[4])
    return render_template('confirmacion.html', dog=dog_obj)

@main_bp.route('/procesar_adopcion', methods=['POST'])
def procesar_adopcion():
    """Lógica para validar identidad y registrar la adopción"""
    dog_id = request.form.get('dog_id')
    nombre = request.form.get('name')
    apellido = request.form.get('lastname')
    cedula = request.form.get('id_card')
    direccion = request.form.get('address')
    
    # Verificamos si el usuario ya confirmó su identidad en la pantalla intermedia
    confirmado = request.form.get('confirmado') == 'true'

    if not confirmado:
        # 1. Verificar si la cédula ya existe en MariaDB
        persona_existente = database.check_adopter_by_id_card(cedula)
        
        if persona_existente:
            # 2. Si existe, mostramos la pantalla de "Vigilar Identidad"
            # Pasamos persona_existente (nombre, apellido) y los datos actuales del form
            return render_template('verificar_identidad.html', 
                                 persona=persona_existente, 
                                 datos_form=request.form)

    # 3. Si es una cédula nueva o ya confirmó, procesamos la transacción
    exito = database.register_adoption_transactional(dog_id, nombre, apellido, direccion, cedula)
    
    if exito:
        # REDIRIGIMOS a una ruta limpia para evitar duplicados al refrescar (F5)
        return redirect(url_for('main.pantalla_exito'))
    else:
        # En caso de error (como perro ya adoptado), podrías usar flash() o un mensaje simple
        return "Error al procesar la adopción. Es posible que el perrito ya haya sido adoptado.", 500

@main_bp.route('/exito')
def pantalla_exito():
    """Ruta final de agradecimiento (evita reenvío de formularios)"""
    return render_template('exito.html')

@main_bp.route('/historial')
def historial():
    """Lista de todas las adopciones realizadas"""
    adopciones = database.get_adoption_history()
    return render_template('historial.html', adopciones=adopciones)