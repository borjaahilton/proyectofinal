from app import create_app
from db import get_db

def reproduce():
    app = create_app()
    with app.app_context():
        db = get_db()
        print("1. Creating Test Data...")
        # Create Product
        try:
            db.execute('INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)', ('Test Shoe', 100.00, 10))
            pid = db.connection.cursor().lastrowid # hack to get lastrowid from raw connector if wrapper doesn't support property on cursor object matching this usage
            # Actually wrapper returns a MySQLCursorWrapper which has lastrowid property
        except Exception:
            # Maybe it exists? Get an ID
            pass
            
        # Get a product ID
        p = db.execute('SELECT id_producto FROM productos LIMIT 1').fetchone()
        if not p:
             print("Failed to create product")
             return
        pid = p['id_producto']
        print(f"Product ID: {pid}")

        # Get a user ID
        u = db.execute('SELECT id_usuario FROM usuarios LIMIT 1').fetchone()
        if not u:
             print("No users found. Creating one.")
             db.execute("INSERT INTO usuarios (nombre, correo, contraseña) VALUES ('Test', 'test@test.com', '123')")
             u = db.execute('SELECT id_usuario FROM usuarios LIMIT 1').fetchone()
        uid = u['id_usuario']
        print(f"User ID: {uid}")

        # Create Sale
        print("Creating Sale...")
        cur = db.execute('INSERT INTO ventas (id_usuario, total, estado) VALUES (%s, %s, %s)', (uid, 200.00, 'pendiente'))
        sale_id = cur.lastrowid
        print(f"Sale ID: {sale_id}")
        db.commit()

        # Create Detail
        print("Creating Detail...")
        db.execute('INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) VALUES (%s, %s, %s, %s)', 
                   (sale_id, pid, 2, 200.00))
        db.commit()

        print("2. Testing Admin Query (Sale Detail)...")
        try:
            sale = db.execute('''
                SELECT v.*, u.nombre, u.apellido, u.correo, u.direccion, u.telefono
                FROM ventas v
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                WHERE v.id_venta = %s
            ''', (sale_id,)).fetchone()
            print(f"Sale Fetched: {sale is not None}")
            if sale:
                print(f"Sale keys: {sale.keys()}")
            
            items = db.execute('''
                SELECT d.*, p.nombre as producto_nombre
                FROM detalle_venta d
                JOIN productos p ON d.id_producto = p.id_producto
                WHERE d.id_venta = %s
            ''', (sale_id,)).fetchall()
            print(f"Items Fetched: {len(items)}")
            if len(items) > 0:
                print(f"First Item keys: {items[0].keys()}")
                print(f"Product Name: {items[0]['producto_nombre']}")

            print("\nSUCCESS: No crash observed in queries.")
        except Exception as e:
            print(f"\nCRASH DETECTED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    reproduce()
