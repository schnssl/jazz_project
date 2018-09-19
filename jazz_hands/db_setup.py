# import os
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# file_path = os.path.join(os.path.abspath(os.getcwd()), 'testing_db.db')
#
# engine = create_engine('sqlite:///' + file_path, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
#
# def init_db():
#     Base.metadata.create_all(bind=engine)
