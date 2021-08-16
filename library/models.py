from . import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    published_date = db.Column(db.Date(), nullable=False)
    ISBN = db.Column(db.Integer, nullable=False, unique=True)
    num_pages = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.Text)
    language = db.Column(db.String(80), nullable=False)

    def __str__(self):
        return f"{self.__dict__}"
