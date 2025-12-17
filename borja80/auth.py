import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM usuarios WHERE correo = ?', (correo,)
        ).fetchone()

        if user is None:
            error = 'Correo incorrecto.'
        elif user['contraseña'] != password and not check_password_hash(user['contraseña'], password):
             # Checks plain text first (for seed admin), then hash
             error = 'Contraseña incorrecta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id_usuario']
            session['user_tipo'] = user['tipo']
            
            # Load logged in user into g immediately for this request if needed, 
            # though redirect happens next.
            
            if user['tipo'] == 'administrador':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('client.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuarios WHERE id_usuario = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('client.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user['tipo'] != 'administrador':
             flash("Acceso denegado. Solo administradores.")
             return redirect(url_for('client.index'))
        return view(**kwargs)
    return wrapped_view
