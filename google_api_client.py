import requests
from library.models import Book
from library import db
from datetime import datetime


def call_google_api(endpoint):
    full_url = f"https://www.googleapis.com/books/v1/volumes{endpoint}"
    response = requests.get(full_url)
    response.raise_for_status()
    return response.json()


def results_to_db(results):
    for result in results:
        print(result)
        book = result['volumeInfo']
        try:
            title = book['title']
            isbn = book['industryIdentifiers'][0]['identifier']
            a = ""
            for author in book['authors']:
                a += f"{author}, "
            a = a[:-2]
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
                pub_date = datetime.strptime(pub_date, '%Y', '%m')
            except ValueError:
                pub_date = datetime.strptime(pub_date, '%Y')
        try:
            cover_url = book['imageLinks']['smallThumbnail']
        except KeyError:
            cover_url = ""

        b = Book(title=title,
                 author=a,
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