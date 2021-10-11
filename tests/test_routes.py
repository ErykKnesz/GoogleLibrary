from unittest.mock import MagicMock
from library import app
from werkzeug.datastructures import ImmutableMultiDict
from library.models import Book, Author
from datetime import date


def test_homepage():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_add_book_with_get():
    with app.test_client() as client:
        response = client.get('add-book')
        assert response.status_code == 200


def test_add_book_with_post():
    with app.test_client() as client:
        response = client.post('/add-book')
        assert response.status_code == 200


def test_edit_book_with_get(monkeypatch):
    db_mock = MagicMock()
    monkeypatch.setattr("flask_sqlalchemy._QueryProperty.__get__", db_mock)
    with app.test_client() as client:
        response = client.get('/edit-book/1')
        assert response.status_code == 200
        db_mock.assert_called_once()


def test_edit_book_with_post(monkeypatch):
    db_mock = MagicMock()
    monkeypatch.setattr("flask_sqlalchemy._QueryProperty.__get__", db_mock)
    with app.test_client() as client:
        response = client.post('/edit-book/1')
        assert response.status_code == 200
        db_mock.assert_called_once()


def test_search_google_api_loads():
    with app.test_client() as client:
        response = client.get('/search-google-api')
        assert response.status_code == 200


def test_search_google_api_performs_search(monkeypatch):
    api_mock = MagicMock()
    search_query = ImmutableMultiDict([('q', ''), ('intitle', 'lalka')])
    monkeypatch.setattr("google_api_client.search", api_mock)
    with app.test_client() as client:
        response = client.get('/search-google-api?q=&intitle=lalka')
        assert response.status_code == 302
        api_mock.assert_called_once_with(search_query)


def test_get_books(monkeypatch):
    db_mock = MagicMock()
    author = Author(name='Guido')
    db_mock.return_value = [Book(title='a',
                                 authors=[author],
                                 ISBN=1111111111,
                                 published_date=date(1, 1, 1),
                                 num_pages=1,
                                 language='pl'
                                 )]
    monkeypatch.setattr("database_service.get_books", db_mock)
    with app.test_client() as client:
        response = client.get('/api/v1/books')
        assert response.status_code == 200
        db_mock.assert_called_once()