from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from auth import admin_required
from db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    # Basic stats
    # Basic stats
    # Use aliases for dictionary access
    product_count = db.execute('SELECT COUNT(*) as count FROM productos').fetchone()['count']
    sale_count = db.execute('SELECT COUNT(*) as count FROM ventas').fetchone()['count']
    try:
        total_income = db.execute('SELECT SUM(total) as total FROM ventas WHERE estado != "cancelado"').fetchone()['total'] or 0
    except:
        total_income = 0
        
    return render_template('admin/dashboard.html', 
                           product_count=product_count, 
                           sale_count=sale_count, 
                           total_income=total_income)

@bp.route('/products')
@admin_required
def products():
    db = get_db()
    products = db.execute(
        'SELECT * FROM productos ORDER BY fecha_ingreso DESC'
    ).fetchall()
    return render_template('admin/products.html', products=products)

@bp.route('/products/create', methods=('GET', 'POST'))
@admin_required
def create_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        talla = request.form['talla']
        color = request.form['color']
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion']
        imagen = request.form['imagen'] # URL or path

        error = None

        if not nombre or not precio:
            error = 'Name and Price are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO productos (nombre, marca, talla, color, precio, stock, descripcion, imagen) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (nombre, marca, talla, color, precio, stock, descripcion, imagen)
            )
            db.commit()
            return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html')

@bp.route('/products/<int:id>/update', methods=('GET', 'POST'))
@admin_required
def update_product(id):
    db = get_db()
    product = db.execute('SELECT * FROM productos WHERE id_producto = ?', (id,)).fetchone()

    if product is None:
        abort(404, f"Product id {id} doesn't exist.")

    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        talla = request.form['talla']
        color = request.form['color']
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion']
        imagen = request.form['imagen']

        error = None

        if not nombre or not precio:
            error = 'Name and Price are required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE productos SET nombre = ?, marca = ?, talla = ?, color = ?, precio = ?, stock = ?, descripcion = ?, imagen = ? WHERE id_producto = ?',
                (nombre, marca, talla, color, precio, stock, descripcion, imagen, id)
            )
            db.commit()
            return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=product)

@bp.route('/products/<int:id>/delete', methods=('POST',))
@admin_required
def delete_product(id):
    db = get_db()
    db.execute('DELETE FROM productos WHERE id_producto = ?', (id,))
    db.commit()
    return redirect(url_for('admin.products'))

@bp.route('/sales')
@admin_required
def sales():
    db = get_db()
    # Join with users to show who bought it
    sales = db.execute('''
        SELECT v.id_venta, v.fecha_venta, v.total, v.estado, u.nombre, u.apellido 
        FROM ventas v 
        JOIN usuarios u ON v.id_usuario = u.id_usuario 
        ORDER BY v.fecha_venta DESC
    ''').fetchall()
    return render_template('admin/sales.html', sales=sales)

@bp.route('/sales/<int:id>')
@admin_required
def sale_detail(id):
    db = get_db()
    sale = db.execute('''
        SELECT v.*, u.nombre, u.apellido, u.correo, u.direccion, u.telefono
        FROM ventas v
        JOIN usuarios u ON v.id_usuario = u.id_usuario
        WHERE v.id_venta = ?
    ''', (id,)).fetchone()

    if sale is None:
        abort(404)

    items = db.execute('''
        SELECT d.*, p.nombre as producto_nombre
        FROM detalle_venta d
        JOIN productos p ON d.id_producto = p.id_producto
        WHERE d.id_venta = ?
    ''', (id,)).fetchall()

    return render_template('admin/sale_detail.html', sale=sale, items=items)
