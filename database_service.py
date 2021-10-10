from datetime import date
from sqlalchemy import or_
from library.models import Book, Author
from library import db


def get_books(request):
    filters = {key: value for key, value in request.args.items() if value}
    search_type = filters.pop('search', None)
    if 'authors' in filters:
        name = filters.pop('authors')
        filters['name'] = name
    if filters:

        if search_type == 'filter':
            min_date = filters.pop('min date', date(1, 1, 1))
            max_date = filters.pop('max date', date(9999, 1, 1))
            books = Book.query.join(Book.authors).filter_by(
                **filters).filter(Book.published_date.between(
                    min_date, max_date)).all()

        elif search_type == 'search':
            search_args = []
            columns = [col for col in Book.__table__.columns]
            columns += list(Author.__table__.columns)
            for col in columns:
                for k, v in filters.items():
                    if col.key in filters.keys():
                        q = col.ilike('%%%s%%' % v)
                        search_args.append(q)
            books = Book.query.join(Book.authors).filter(
                or_(*search_args)).all()

    else:
        books = Book.query.all()
    return books

