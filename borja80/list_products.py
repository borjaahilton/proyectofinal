from app import create_app
from db import get_db

def list_products():
    app = create_app()
    with app.app_context():
        db = get_db()
        products = db.execute('SELECT id_producto, nombre, color FROM productos').fetchall()
        for p in products:
            print(f"ID: {p['id_producto']} | Name: {p['nombre']} | Color: {p['color']}")

if __name__ == '__main__':
    list_products()
