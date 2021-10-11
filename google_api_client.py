from datetime import datetime
from urllib.parse import urljoin

import requests

from library.models import Book, Author
from library import db


def call_google_api(endpoint):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    full_url = urljoin(base_url, endpoint)
    response = requests.get(full_url)
    response.raise_for_status()
    return response.json()


def results_to_db(results):
    for result in results:
        book = result['volumeInfo']
        try:
            title = book['title']
            isbn = book['industryIdentifiers'][0]['identifier']
            authors = []
            for author in book['authors']:
                a = (Author(name=author) if not
                     Author.query.filter_by(name=author).first()
                     else Author.query.filter_by(name=author).first()
                     )
                db.session.add(a)
                db.session.commit()
                authors.append(a)
            pub_date = book['publishedDate']
            num_pages = book['pageCount']
            language = book['language']
        except KeyError:
            continue

        if (Book.query.filter_by(title=title).first() or
                Book.query.filter_by(ISBN=isbn).first()):
            continue

        try:
            pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
        except ValueError:
            try:
                pub_date = datetime.strptime(pub_date, '%Y-%m')
            except ValueError:
                pub_date = datetime.strptime(pub_date, '%Y')
        try:
            cover_url = book['imageLinks']['smallThumbnail']
        except KeyError:
            cover_url = ""

        b = Book(title=title,
                 authors=authors,
                 published_date=pub_date,
                 ISBN=isbn,
                 num_pages=num_pages,
                 cover_url=cover_url,
                 language=language
                 )
        db.session.add(b)
        db.session.commit()


def search(search_query):
    query_start = search_query.get('q')
    full_query = f"?q={query_start}"
    for key, value in search_query.items():
        if key != 'q' and value:
            full_query += f"+{key}{value}"
    results = call_google_api(full_query)
    if results['totalItems'] > 0:
        results = results['items']
    else:
        results = ""
    return results
