from app import create_app
from db import get_db

app = create_app()

with app.app_context():
    db = get_db()
    print("Updating admin user...")
    try:
        # Delete existing admins to avoid duplicates
        db.execute("DELETE FROM usuarios WHERE tipo='administrador'")
        db.commit()
        print("Old admins deleted.")
        
        # Insert fresh admin
        db.execute("INSERT INTO usuarios (nombre, apellido, correo, contraseña, tipo) VALUES ('System', 'Admin', 'ADMIN', '1234', 'administrador')")
        db.commit()
        print("New ADMIN user created successfully.")
             
    except Exception as e:
        print(f"Error: {e}")
