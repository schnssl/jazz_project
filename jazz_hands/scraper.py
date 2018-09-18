import requests
import unicodedata
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
resp = requests.get('https://www.jazzdisco.org/blue-note-records/catalog-4000-series/', headers=headers)
html_doc = resp.content.decode()
soup = BeautifulSoup(html_doc, 'html.parser')

entries = soup.find_all('h3')
db = []

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

        text = t.next_sibling[1:-2]
        raw_lineup = text.split('; ')
        clean_lineup = {}
        for member in raw_lineup:
            items = member.split(', ')
            player = items[0]
            instrument = items[1]
            if instrument not in clean_lineup.keys():
                clean_lineup[instrument] = player
            else:
                print(title)

        entry = {'catalogue_number': cat_num, 'artist': artist, 'title': title, 'year': year,
                 'line_up': clean_lineup
                 }

        db.append(entry)
    except:
        print(text)


instruments = []
for e in db:
    band = e['line_up']
    for k in band.keys():
        k_clean = k.split(' #')[0]
        if k_clean not in instruments:
            instruments.append(k_clean)
