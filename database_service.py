from library.models import Book
from datetime import date


def get_books(request):
    filters = {key: value for key, value in request.args.items() if value}
    if filters:
        min_date = filters.pop('min date', date(1, 1, 1))
        max_date = filters.pop('max date', date(9999, 1, 1))
        books = Book.query.filter_by(**filters).filter(
            Book.published_date.between(
                min_date, max_date)
        )
    else:
        books = Book.query.all()
    return books
