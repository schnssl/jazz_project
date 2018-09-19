import sqlite3

from flask import g


DATABASE = 'jazz_hands/testing_db.sqlite'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return db


def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
