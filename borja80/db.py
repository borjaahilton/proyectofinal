import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext

class MySQLWrapper:
    """Wrapper to make MySQL connector behave like SQLite for this app (parsing ? to %s)"""
    def __init__(self, connection):
        self.connection = connection

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        cursor = self.connection.cursor(dictionary=True)
        # SQLite uses ?, MySQL uses %s. Simple replace.
        sql = sql.replace('?', '%s')
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return MySQLCursorWrapper(cursor)
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            print(f"Failed SQL: {sql}")
            raise err

class MySQLCursorWrapper:
    """Wrapper to expose fetchone/fetchall/lastrowid behaving like SQLite cursor"""
    def __init__(self, cursor):
        self.cursor = cursor
    
    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    @property
    def lastrowid(self):
        return self.cursor.lastrowid

def get_db():
    if 'db' not in g:
        # ---------------------------------------------------------
        # CONFIGURA TUS CREDENCIALES DE MYSQL AQUÍ
        # REPLACE WITH YOUR ACTUAL MYSQL CREDENTIALS
        # ---------------------------------------------------------
        db_config = {
            'host': 'localhost',
            'user': 'root',           # Usuario por defecto común
            'password': '',           # Contraseña vacía por defecto
            'database': 'urban_kicks'
        }
        
        try:
            conn = mysql.connector.connect(**db_config)
            g.db = MySQLWrapper(conn)
        except mysql.connector.Error as err:
            # If DB doesn't exist, try connecting without DB to create it?
            # For now just raise
            print(f"Error connecting to MySQL: {err}")
            raise err

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    # Direct connection to create DB if not exists (raw usage)
    # NOTE: This simple init script assumes the user has permissions. 
    # It might be safer for the user to create the DB manually 'CREATE DATABASE urban_kicks;'
    pass

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    # For MySQL migration, we often assume the DB is managed externally or via migration tools.
    # We will print instructions here or try to run schema if connected.
    
    # Reading schema.sql to run split commands
    try:
        db = get_db()
        with current_app.open_resource('schema.sql') as f:
            script = f.read().decode('utf8')
            commands = script.split(';')
            for cmd in commands:
                if cmd.strip():
                    db.execute(cmd)
        click.echo('Initialized the database.')
    except Exception as e:
        click.echo(f'Error initializing database: {e}')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
