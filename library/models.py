from . import db

association_table = db.Table(
    'association',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'),
              primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'),
              primary_key=True)
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    authors = db.relationship("Author", lazy='subquery',
                              secondary=association_table,
                              backref=db.backref('books', lazy=True))
    published_date = db.Column(db.Date(), nullable=False)
    ISBN = db.Column(db.Integer, nullable=False, unique=True)
    num_pages = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.Text)
    language = db.Column(db.String(2), nullable=False)

    def __str__(self):
        return f"{self.__dict__}"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name
