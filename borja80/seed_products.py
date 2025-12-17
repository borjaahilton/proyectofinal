from app import create_app
from db import get_db

def seed_products():
    app = create_app()
    with app.app_context():
        db = get_db()
        
        # 1. Rename Test Shoe to something real
        db.execute('UPDATE productos SET nombre="New Balance 550", precio=120.00, color="White/Green" WHERE nombre="Test Shoe"')
        # Note: If Test Shoe doesn't exist (deleted), we insert it.
        
        products = [
            ("Air Jordan 1 High", "Nike", "10", "Chicago", 180.00, 15, "Classic high-top basketball sneaker."),
            ("Yeezy Boost 350", "Adidas", "9", "Onyx", 230.00, 8, "Comfortable knit lifestyle sneaker."),
            ("Air Max 90", "Nike", "11", "Infrared", 130.00, 20, "Retro running shoe with visible air."),
            ("Ultraboost 1.0", "Adidas", "10.5", "Triple White", 190.00, 12, "High performance running shoe.")
        ]
        
        for p in products:
            # Check if exists to avoid dupes on re-run
            exists = db.execute('SELECT id_producto FROM productos WHERE nombre = %s', (p[0],)).fetchone()
            if not exists:
                db.execute(
                    'INSERT INTO productos (nombre, marca, talla, color, precio, stock, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    p
                )
                print(f"Inserted {p[0]}")
            else:
                print(f"Skipped {p[0]}")
        
        db.commit()

if __name__ == '__main__':
    seed_products()
