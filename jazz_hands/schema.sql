DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS band;

CREATE TABLE album (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    catalogue_number TEXT,
    record_label TEXT,
    title TEXT NOT NULL,
    release_year DATE NOT NULL,
    leader TEXT NOT NULL,
    band_id INTEGER NOT NULL
    FOREIGN KEY (band_id) REFERENCES band (id)
);

CREATE TABLE band (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    player TEXT NOT NULL,
    instrument TEXT NOT NULL,
    FOREIGN KEY (album_id) REFERENCES album (id)
);

