import config

# Lista con los nombres exactos de tus perritos
nombres_perritos = ["Luna", "Coco", "Bella", "Toby", "Daisy", "Rocky", "Nala", "Bruno", "Maya", "Simba"]

conn = config.get_db_connection()
cur = conn.cursor()

for nombre in nombres_perritos:
    # Creamos la ruta local para Flask (ejemplo: /static/img/luna.jpg)
    # .lower() convierte el nombre a minúsculas para que coincida con el archivo
    ruta_local = f"/static/img/{nombre.lower()}.jpg" 
    
    cur.execute("UPDATE Dog SET image_url = ? WHERE name = ?", (ruta_local, nombre))

conn.commit()
conn.close()

print("🐾 ¡Rutas de imágenes locales actualizadas en la base de datos!") 