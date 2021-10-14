from datetime import date
from sqlalchemy import or_
from library.models import Book, Author
from library import db


def get_books(request):
    filters = {key: value for key, value in request.args.items()
               if value and key != 'page'}
    search_type = filters.pop('search', None)
    if 'authors' in filters:
        name = filters.pop('authors')
        filters['name'] = name
    if filters:
        min_date = filters.pop('min date', date(1, 1, 1))
        max_date = filters.pop('max date', date(9999, 1, 1))
        if search_type == 'filter':
            if 'name' in filters:
                name = filters.pop('name')
            books = Book.query.filter_by(
                **filters).join(Book.authors)
            try:
                books = books.filter_by(name=name)
            except UnboundLocalError:
                pass

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
                or_(*search_args))

        books = books.filter(Book.published_date.between(
                    min_date, max_date))
    else:
        books = Book.query.join(Book.authors)

    return books.order_by(Author.name.asc())


def preprocess_form_authors(form):
    form.authors.data = form.authors.data.split(', ')
    for i, name in enumerate(form.authors.data):
        author = Author.query.filter_by(name=name).first()
        if author:
            form.authors.data[i] = author
        else:
            author = Author(name=name)
            db.session.add(author)
            db.session.commit()
            form.authors.data[i] = author
    return form.authors.data
