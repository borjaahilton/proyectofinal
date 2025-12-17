from app import create_app
from db import get_db

def update_images():
    app = create_app()
    with app.app_context():
        db = get_db()
        # Update Product 1 (Dunk Low)
        print("Updating Product 1...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/dunk_low.jpg', 1))

        # Update Product 2 (Future)
        print("Updating Product 2...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/orange_cleat.png', 2))

        # Update Product 3 (Mercurial)
        print("Updating Product 3...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/mercurial.png', 3))

        # Update Product 5 (Strange name)
        print("Updating Product 5...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/brown_casual.png', 5))

        # Update Product 9 (NB 550 Grey)
        print("Updating Product 9...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/nb_grey.png', 9))

        # Update Product 10 (NB 550 Teal)
        print("Updating Product 10...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/nb_teal.png', 10))

        # Update Product 11 (AJ1)
        print("Updating Product 11...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/aj1_red.png', 11))

        # Update Product 12 (Yeezy Boost 350)
        print("Updating Product 12...")
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto = %s", ('/static/images/yeezy_boost.png', 12))

        db.commit()
        print("Images updated successfully.")

if __name__ == '__main__':
    update_images()
