from . import db


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    ISBN = db.Column(db.Integer, nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(80), nullable=False)
