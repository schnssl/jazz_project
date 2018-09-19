import sqlite3

import requests
import unicodedata
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
resp = requests.get('https://www.jazzdisco.org/blue-note-records/catalog-4000-series/', headers=headers)
html_doc = resp.content.decode()
soup = BeautifulSoup(html_doc, 'html.parser')

entries = soup.find_all('h3')
db = sqlite3.connect(
            "C:/Users/johan/Documents/jazz_project/testing_db.db")

i = 1
for t in entries:
    text = t.text
    try:
        clean_text = unicodedata.normalize('NFKD', text)
        text_items = clean_text.split('   ')
        cat_num = text_items[0]
        name = text_items[1].split(' - ')
        artist = name[0]
        title = name[1]
        year = text_items[2]

        db.execute('INSERT INTO album (catalogue_number, record_label, title, release_year, leader)'
                   ' VALUES (?, ?, ?, ?, ?)', (cat_num, 'Blue Note', title, year, artist))
        db.commit()

        text = t.next_sibling[1:-2]
        raw_lineup = text.split('; ')
        clean_lineup = {}
        for member in raw_lineup:
            items = member.split(', ')
            player = items[0]
            instrument = items[1]
            clean_instrument = instrument.split(' #')[0]

            db.execute('INSERT INTO band (album_id, player, instrument)'
                       ' VALUES (?, ?, ?)', (i, player, clean_instrument))
            db.commit()

        i += 1
    except:
        pass