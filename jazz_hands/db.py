import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


DATABASE = 'jazz_hands/testing_db.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row

    return db

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db


def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()
#
#
# def init_db():
#     db = get_db()
#
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf-8'))
#
#
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     # Clear the existing data and create new tables
#     init_db()
#     click.echo('Initialized the database')
#
#

