from unittest.mock import Mock
from werkzeug.datastructures import ImmutableMultiDict
import google_api_client as gac


def test_call_google_api(monkeypatch):
    mock_books = ['book 1', 'book 2']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_books
    monkeypatch.setattr("google_api_client.requests.get", requests_mock)
    url = "https://www.googleapis.com/books/v1/volumes"
    books = gac.call_google_api(url)
    assert books == mock_books


def test_search(monkeypatch):
    mock = Mock(return_value={'totalItems': 1,
                'items': []})
    mock_result = mock.return_value['items']
    monkeypatch.setattr("google_api_client.call_google_api", mock)
    search_query = ImmutableMultiDict([('q', ''), ('intitle', 'lalka')])
    result = gac.search(search_query)
    assert mock_result == result