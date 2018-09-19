import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from . import db_setup


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///jazz_hands/testing_db.sqlite',
)

# if test_config is None:
#     # Load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # Load the test config if passed in
#     app.config.from_mapping(test_config)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db = SQLAlchemy(app)

from . import search
app.register_blueprint(search.bp)
app.add_url_rule('/', endpoint='index')


# A simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'
