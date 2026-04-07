import mariadb
import config

def get_db_connection():
    return config.get_db_connection()

def get_available_dogs():
    conn = get_db_connection()
    cur = conn.cursor()
    # Solo traemos perros que NO han sido adoptados
    cur.execute("SELECT id, name, breed, age, image_url FROM Dog WHERE adopted = 0")
    dogs = cur.fetchall()
    conn.close()
    return dogs

def get_dog_by_id(dog_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, breed, age, image_url FROM Dog WHERE id = %s", (dog_id,))
    dog = cur.fetchone()
    conn.close()
    return dog

def check_adopter_by_id_card(id_card):
    """Busca si la cédula ya existe para la validación de identidad"""
    conn = get_db_connection()
    cur = conn.cursor()
    # Importante: Usar el nombre de columna exacto 'lastName'
    cur.execute("SELECT name, lastName FROM Person WHERE id_card = %s", (id_card,))
    person = cur.fetchone()
    conn.close()
    return person

def register_adoption_transactional(dog_id, adopter_name, adopter_lastname, address, id_card):
    """Proceso atómico de adopción"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 1. Verificar si la persona ya existe para no duplicarla
        cur.execute("SELECT id FROM Person WHERE id_card = %s", (id_card,))
        existing_person = cur.fetchone()

        if existing_person:
            person_id = existing_person[0]
        else:
            # Insertar nueva persona (lastName con N mayúscula como en tu tabla)
            cur.execute("INSERT INTO Person (name, lastName, id_card) VALUES (%s, %s, %s)", 
                       (adopter_name, adopter_lastname, id_card))
            person_id = cur.lastrowid
            
            # Insertar en tabla Adopter
            cur.execute("INSERT INTO Adopter (person_id, address) VALUES (%s, %s)", 
                       (person_id, address))

        # 2. Registrar la adopción (Usamos %s para MariaDB)
        cur.execute("INSERT INTO Adoption (adopter_id, dog_id) VALUES (%s, %s)", 
                   (person_id, dog_id))

        # 3. Marcar al perro como adoptado
        cur.execute("UPDATE Dog SET adopted = 1 WHERE id = %s", (dog_id,))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error en transacción: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_adoption_history():
    conn = get_db_connection()
    cur = conn.cursor()
    # El orden es: 0:Nombre, 1:Apellido, 2:URL_Foto, 3:Nombre_Perro, 4:Raza, 5:Fecha
    query = """
        SELECT p.name, p.lastName, d.image_url, d.name, d.breed, a.adoption_date
        FROM Adoption a
        JOIN Person p ON a.adopter_id = p.id
        JOIN Dog d ON a.dog_id = d.id
        ORDER BY a.adoption_date DESC
    """
    cur.execute(query)
    history = cur.fetchall()
    conn.close()
    return history