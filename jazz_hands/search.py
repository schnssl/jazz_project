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


def generate_network_layer(df, network_above):
    albums = df.loc[df['player'].isin(network_above), 'album_id'].unique()
    network = df.loc[(df['album_id'].isin(albums)) & ~(df['player'].isin(network_above)), 'player'].value_counts()

    return network


SCORE_CONST = 20
NET_RANGE = 3


def rank_records(df, network):
    df['score'] = 0

    df.loc[df['player'].isin(network), 'score'] = SCORE_CONST
    for i in range(1, NET_RANGE + 1):
        network = generate_network_layer(df, network)
        df['score'] = df.apply(lambda x:
                               network[network.index == x.player].values[0] / i
                               if x.player in network.index
                               and x.score < network[network.index == x.player].values[0] / i
                               else x.score,
                               axis=1)

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
