# import sqlite3
#
# from flask import g
#
#
# DATABASE = 'jazz_hands/testing_db.sqlite'
#
#
# def get_db():
#     db = getattr(g, 'db', None)
#     if db is None:
#         db = g.db = sqlite3.connect(DATABASE)
#         g.db.row_factory = sqlite3.Row
#
#     return db
#
#
# def close_db(e=None):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///jazz_hands/testing_db.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
