from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wtforms import Form, StringField
from flask_table import Table, Col

# from jazz_hands.db import get_db
from .app import db
from .models import Album

bp = Blueprint('search', __name__)


class PlayerSearchForm(Form):
    search = StringField('Search for records with these players in the line-up (separated by commas): ')


class Results(Table):
    id = Col('id', show=False)
    record_label = Col('record_label')
    catalogue_number = Col('catalogue_number')
    title = Col('title')
    release_year = Col('release_year')
    leader = Col('leader')


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

    if len(players) < 2:
        return redirect('/')

    results = Album.query.all()
    # db = get_db()
    # results = db.engine.execute(
    #     """SELECT * FROM album
    #         WHERE id =
    #       (SELECT album_id FROM band
    #         WHERE player IN (?, ?)
    #         GROUP BY album_id
    #        HAVING COUNT(DISTINCT player) = ?)""",
    #     (players[0], players[1], len(players))
    # )

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
