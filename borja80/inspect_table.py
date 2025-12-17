from db import get_db
from app import create_app

def inspect():
    app = create_app()
    with app.app_context():
        db = get_db()
        # raw cursor to describe
        try:
            res = db.execute("DESCRIBE detalle_venta").fetchall()
            print("Columns in detalle_venta:")
            for r in res:
                # Field is usually the first key or 'Field'
                print(f"COLUMN: {r['Field']}")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    inspect()
