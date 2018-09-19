from .app import db


class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    catalogue_number = db.Column(db.String)
    record_label = db.Column(db.String)
    title = db.Column(db.String)
    release_year = db.Column(db.String)
    leader = db.Column(db.String)


class Band(db.Model):
    __tablename__ = 'band'

    row_id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    player = db.Column(db.String)
    instrument = db.Column(db.String)