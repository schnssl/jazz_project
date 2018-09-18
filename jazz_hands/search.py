from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wtforms import Form, StringField


from jazz_hands.db import get_db

bp = Blueprint('search', __name__)


class PlayerSearchForm(Form):
    search = StringField('Search for records with these players in the line-up (separated by commas): ')


@bp.route('/', methods=('GET', 'POST'))
def index():
    search_query = PlayerSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search_query)

    return render_template('index.html', form=search_query)


@bp.route('/results', methods=('GET',))
def search_results(search_query):
    search_string = search_query.data['search']
    players = search_string.split(', ')

    if not len(search_string):
        return redirect('/')

    db = get_db()
    results = db.execute(
        """SELECT * FROM album 
            WHERE id = 
          (SELECT album_id FROM band
            WHERE player IN (?, ?)
            GROUP BY album_id
           HAVING COUNT(DISTINCT player) = ?)""",
        (players[0], players[1], len(players))
    ).fetchall()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('results.html', results=results)
