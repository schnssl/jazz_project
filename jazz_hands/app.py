import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

file_path = os.path.join(os.path.abspath(os.getcwd()), 'testing_db.db')

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + file_path,
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db = SQLAlchemy(app)

from . import search
app.register_blueprint(search.bp)
app.add_url_rule('/', endpoint='index')

