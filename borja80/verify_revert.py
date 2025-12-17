from app import create_app
from db import get_db
import os

def verify_revert():
    app = create_app()
    with app.app_context():
        db = get_db()
        # Check database
        products = db.execute("SELECT id_producto, nombre, imagen FROM productos WHERE id_producto IN (1, 14)").fetchall()
        print("Checking Database...")
        for p in products:
            print(f"Product: {p['nombre']} | Image: {p['imagen']}")
            
        # Check files
        static_folder = os.path.join(app.root_path, 'static')
        gen_files = [
            os.path.join(static_folder, 'img', 'products', 'product_1.png'),
            os.path.join(static_folder, 'img', 'products', 'product_14.png')
        ]
        
        print("\nChecking File Deletion...")
        for gf in gen_files:
            if os.path.exists(gf):
                print(f"WARNING: File still exists: {gf}")
            else:
                print(f"OK: File gone: {gf}")

if __name__ == '__main__':
    verify_revert()
