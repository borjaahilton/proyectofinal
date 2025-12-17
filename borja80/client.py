from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from db import get_db
import datetime

bp = Blueprint('client', __name__)

@bp.route('/')
def index():
    db = get_db()
    products = db.execute('SELECT * FROM productos WHERE stock > 0').fetchall()
    return render_template('client/index.html', products=products)

@bp.route('/product/<int:id>')
def product(id):
    db = get_db()
    product = db.execute('SELECT * FROM productos WHERE id_producto = ?', (id,)).fetchone()
    return render_template('client/product.html', product=product)

@bp.route('/cart')
def cart():
    # Simple cart using session
    # Cart structure in session: {'product_id': quantity, ...}
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    db = get_db()
    
    for pid, qty in cart.items():
        p = db.execute('SELECT * FROM productos WHERE id_producto = ?', (pid,)).fetchone()
        if p:
            subtotal = p['precio'] * qty
            total += subtotal
            cart_items.append({
                'product': p,
                'quantity': qty,
                'subtotal': subtotal
            })
            
    return render_template('client/cart.html', items=cart_items, total=total)

@bp.route('/cart/add/<int:id>', methods=('POST',))
def add_to_cart(id):
    quantity = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    # If id is integer, json keys convert to string? Session handles it.
    # We'll normalize to string keys for session consistency
    sid = str(id)
    if sid in cart:
        cart[sid] += quantity
    else:
        cart[sid] = quantity
        
    session.modified = True
    flash('Producto añadido al carrito.')
    return redirect(url_for('client.index'))

@bp.route('/cart/clear')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('client.cart'))

@bp.route('/checkout', methods=('GET', 'POST'))
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('client.index'))
        
    if request.method == 'POST':
        # Customer Info
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        dni = request.form['dni']
        
        db = get_db()
        error = None
        
        # 1. Find or Create User
        user = db.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,)).fetchone()
        user_id = None
        
        if user:
            user_id = user['id_usuario']
            # Optionally update info here? We'll skip for now to avoid overwriting without auth.
        else:
            # Create new user
            # Auto-generate password or ask? We'll auto-generate "123456" for simplicity of prototype
            # as requested "llenado sus datos" implies simple flow.
            # In a real app we'd email them or ask for a password.
            default_pw = "123456" 
            try:
                cur = db.execute(
                    'INSERT INTO usuarios (nombre, apellido, correo, telefono, direccion, contraseña, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (nombre, apellido, correo, telefono, direccion, default_pw, 'cliente')
                )
                user_id = cur.lastrowid
                
                # Also create entry in clientes table
                db.execute(
                    'INSERT INTO clientes (id_usuario, dni, estado) VALUES (?, ?, ?)',
                    (user_id, dni, 'activo')
                )
            except db.IntegrityError:
                error = f"Error creando usuario con correo {correo}."

        if error is None:
            # 2. Create Sale (Venta)
            total = 0
            items_to_insert = []
            
            # Re-calculate total to be safe
            for pid, qty in cart.items():
                p = db.execute('SELECT * FROM productos WHERE id_producto = ?', (pid,)).fetchone()
                if p:
                    subtotal = p['precio'] * qty
                    total += subtotal
                    items_to_insert.append((p['id_producto'], qty, subtotal))
            
            cur = db.execute(
                'INSERT INTO ventas (id_usuario, total, estado) VALUES (?, ?, ?)',
                (user_id, total, 'pendiente') # Payment integration is next step, keeping as pending
            )
            sale_id = cur.lastrowid
            
            # 3. Create Sale Details (Detalle Venta)
            for pid, qty, subtotal in items_to_insert:
                db.execute(
                    'INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)',
                    (sale_id, pid, qty, subtotal)
                )
                
            db.commit()
            session.pop('cart', None)
            flash('¡Compra exitosa! Gracias por tu preferencia.')
            return redirect(url_for('client.index'))
            
        flash(error)
        
    return render_template('client/checkout.html')
