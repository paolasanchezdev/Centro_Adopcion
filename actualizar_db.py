import sqlite3
import config

# Nos conectamos a la base de datos
conn = config.get_db_connection()
cur = conn.cursor()

try:
    # 1. Agregamos la nueva columna a la tabla Dog
    cur.execute("ALTER TABLE Dog ADD COLUMN image_url TEXT;")
    print("✅ Columna 'image_url' creada con éxito.")
except sqlite3.OperationalError:
    print("⚠️ La columna 'image_url' ya existe. Omitiendo este paso.")

# 2. Le ponemos una foto genérica a los perritos que ya están en la base de datos
# (Puedes cambiar estas URLs después directamente en tu base de datos)
foto_perrito = "https://images.unsplash.com/photo-1543466835-00a7907e9de1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60"

cur.execute("UPDATE Dog SET image_url = ? WHERE image_url IS NULL", (foto_perrito,))
conn.commit()
print("✅ Fotos de relleno asignadas a los perritos existentes.")

conn.close()
print("¡Todo listo! Ya puedes correr la aplicación.")