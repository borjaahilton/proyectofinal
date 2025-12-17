import json
from app import create_app
from db import get_db

def list_products_json():
    app = create_app()
    with app.app_context():
        db = get_db()
        products = db.execute('SELECT id_producto, nombre, marca, color, precio FROM productos').fetchall()
        # Convert to list of dicts if not already (MySQLWrapper might return dicts)
        # But handle cases just to be sure
        
        # MySQLWrapper returns dicts if configured, let's assume it does based on db.py
        
        print(json.dumps(products, indent=2, default=str))

if __name__ == '__main__':
    list_products_json()
