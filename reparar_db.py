import config

conn = config.get_db_connection()
cur = conn.cursor()

try:
    print("Iniciando reparación de tablas para MariaDB...")

    # 1. Tabla Person (En MariaDB se usa AUTO_INCREMENT, no AUTOINCREMENT)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            lastName VARCHAR(100) NOT NULL,
            id_card VARCHAR(50) NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (id_card)
        ) ENGINE=InnoDB;
    ''')

    # 2. Tabla Adopter
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Adopter (
            person_id INT NOT NULL,
            address TEXT NOT NULL,
            PRIMARY KEY (person_id),
            CONSTRAINT fk_adopter_person FOREIGN KEY (person_id) REFERENCES Person (id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    ''')

    # 3. Tabla Adoption
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Adoption (
            id INT NOT NULL AUTO_INCREMENT,
            adopter_id INT NOT NULL,
            dog_id INT NOT NULL,
            adoption_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            CONSTRAINT fk_adoption_adopter FOREIGN KEY (adopter_id) REFERENCES Adopter (person_id),
            CONSTRAINT fk_adoption_dog FOREIGN KEY (dog_id) REFERENCES Dog (id)
        ) ENGINE=InnoDB;
    ''')

    conn.commit()
    print("✅ ¡Tablas creadas en MariaDB con éxito!")

except Exception as e:
    print(f"❌ Error al reparar la base de datos: {e}")
finally:
    cur.close()
    conn.close()