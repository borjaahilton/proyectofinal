import os
from app import create_app
from db import get_db

def verify():
    app = create_app()
    with app.app_context():
        db = get_db()
        # Product 3 (Mercurial)
        p3 = db.execute("SELECT imagen FROM productos WHERE id_producto = 3").fetchone()
        print(f"Product 3 image: {p3['imagen']} (Expected: /static/images/mercurial.png)")

        # Product 5 (Strange name)
        p5 = db.execute("SELECT imagen FROM productos WHERE id_producto = 5").fetchone()
        print(f"Product 5 image: {p5['imagen']} (Expected: /static/images/brown_casual.png)")

        # Product 9
        p9 = db.execute("SELECT imagen FROM productos WHERE id_producto = 9").fetchone()
        print(f"Product 9 image: {p9['imagen']} (Expected: /static/images/nb_grey.png)")

        # Product 10
        p10 = db.execute("SELECT imagen FROM productos WHERE id_producto = 10").fetchone()
        print(f"Product 10 image: {p10['imagen']} (Expected: /static/images/nb_teal.png)")

        # Product 11
        p11 = db.execute("SELECT imagen FROM productos WHERE id_producto = 11").fetchone()
        print(f"Product 11 image: {p11['imagen']} (Expected: /static/images/aj1_red.png)")

        # Product 12
        p12 = db.execute("SELECT imagen FROM productos WHERE id_producto = 12").fetchone()
        print(f"Product 12 image: {p12['imagen']} (Expected: /static/images/yeezy_boost.png)")

if __name__ == '__main__':
    verify()
