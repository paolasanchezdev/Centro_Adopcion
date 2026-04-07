import config
conn = config.get_db_connection()
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE Dog ADD COLUMN image_url TEXT;")
    conn.commit()
    print("✅ Columna image_url añadida a la tabla Dog.")
except Exception as e:
    print(f"Aviso: {e} (Tal vez ya existía)")
finally:
    conn.close()