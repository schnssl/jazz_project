import pandas as pd
from flask import (
    Blueprint, flash, redirect, render_template, request
)
from wtforms import Form, StringField
from flask_table import Table, Col

from .app import db

bp = Blueprint('search', __name__)


class PlayerSearchForm(Form):
    search = StringField('Tell us your favorite players so we can suggest some records (separated by commas): ')


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


SCORE = 1
SCORE_1 = 1  # first degree, i.e. is favorite
SCORE_2 = 0.5  # second degree, i.e. played with favorite
SCORE_3 = 0.25  # third degree, i.e. played with favorite's bandmates


# def generate_network_and_score(df, players, degree):
#     df.loc[df['player'].isin(players), 'score'] = SCORE / degree
#     albums = df.loc[df['player'].isin(players), 'album_id'].unique()
#     network = df.loc[(df['album_id'].isin(albums)) & ~(df['player'].isin(players)), 'player'].unique()
#     # Todo return value, dedupe, score network? and implement below
    

def rank_records(df, favorite_players):
    df['score'] = 0
    for fav in favorite_players:
        df.loc[df['player'] == fav, 'score'] = SCORE_1
        fav_albums = df.loc[df['player'] == fav, 'album_id']

        fav_mates = df.loc[(df['album_id'].isin(fav_albums)) & (df['player'] != fav), 'player'].unique()
        df.loc[df['player'].isin(fav_mates), 'score'] = SCORE_2
        fav_albums2 = df.loc[df['player'].isin(fav_mates), 'album_id'].unique()
        fav_albums2_dedupe = [a for a in fav_albums2 if a not in fav_albums]

        fav_mates2 = df.loc[(df['album_id'].isin(fav_albums2_dedupe)) & (df['player'] != fav)
                            & ~(df['player'].isin(fav_mates)), 'player'].unique()
        df.loc[df['player'].isin(fav_mates2), 'score'] = SCORE_3

    res = df.groupby('album_id')['score'].sum()

    return res.sort_values(ascending=False).iloc[:10].index.values


@bp.route('/results', methods=('GET',))
def search_results(search_query):
    search_string = search_query.data['search'].title()
    players = search_string.split(', ')

    if len(players) < 1:
        return redirect('/')

    df = pd.read_sql('SELECT * FROM band', db.engine.connect())
    rank = [int(i) for i in rank_records(df, players)]

    results = db.engine.execute(
        'SELECT * FROM album WHERE id IN'
        ' (' + ','.join('?' * len(rank)) + ')',  # handles different lengths of args,
        rank
    )

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
