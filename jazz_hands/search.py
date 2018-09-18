from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wtforms import Form, StringField


from jazz_hands.db import get_db

bp = Blueprint('search', __name__)


class PlayerSearchForm(Form):
    search = StringField('Search for records with these players in the line-up: ')


@bp.route('/', methods=('GET', 'POST'))
def index():
    search_query = PlayerSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search_query)

    return render_template('index.html', form=search_query)


@bp.route('/results', methods=('GET',))
def search_results(search_query):
    pass

# @bp.route('/create', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None
#
#         if not title:
#             error = 'Title is required'
#
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))
#
#     return render_template('blog/create.html')