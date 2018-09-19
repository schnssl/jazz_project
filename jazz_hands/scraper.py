import sqlite3

import requests
import unicodedata
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
resp = requests.get('https://www.jazzdisco.org/blue-note-records/catalog-4000-series/', headers=headers)
html_doc = resp.content.decode()
soup = BeautifulSoup(html_doc, 'html.parser')

entries = soup.find_all('h3')
conn = sqlite3.connect(
            "C:/Users/johan/Documents/jazz_project/testing_db.db")
cur = conn.cursor()

db_album = []
db_band = []
i = 1
for t in entries:
    text = t.text
    clean_text = unicodedata.normalize('NFKD', text)
    text_items = clean_text.split('   ')
    if text_items[0] == 'List of albums/singles by record number:':
        continue
    cat_num = text_items[0]
    name = text_items[1].split(' - ')
    artist = name[0]
    title = name[1]
    year = 'not released' if 'not released' in title else text_items[2]

    tup = (cat_num, 'Blue Note', title, year, artist)
    db_album.append(tup)

    text = t.next_sibling[1:-2]
    raw_lineup = text.split('; ')
    clean_lineup = {}
    for member in raw_lineup:
        items = member.split(', ')
        if len(items) == 1 and items[0] == '':
            continue
        player = items[0]
        instrument = items[1]
        clean_instrument = instrument.split(' #')[0]
        tup = (i, player, clean_instrument)
        db_band.append(tup)

    i += 1

cur.executemany(
    'INSERT INTO album (catalogue_number, record_label, title, release_year, leader) VALUES (?, ?, ?, ?, ?)',
    db_album)


cur.executemany(
    'INSERT INTO band (album_id, player, instrument) VALUES (?, ?, ?)',
    db_band)
conn.commit()
conn.close()
