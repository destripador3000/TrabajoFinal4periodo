import sqlite3
from flask import current_app, g
import click

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Inicializa la base de datos usando el esquema definido."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Comando de línea para inicializar la base de datos."""
    init_db()
    click.echo('Base de datos inicializada.')

def init_app(app):
    """Registra las funciones de inicialización y cierre en la app Flask."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
