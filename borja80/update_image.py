from app import create_app
from db import get_db

def update_image():
    app = create_app()
    with app.app_context():
        db = get_db()
        # Update Dunk Low image
        db.execute(
            'UPDATE productos SET imagen = %s WHERE nombre LIKE %s', 
            ('http://127.0.0.1:5000/static/images/dunk_low.png', '%dunk low%') 
        )
        db.commit()
        print("Updated Dunk Low image.")

if __name__ == '__main__':
    update_image()
