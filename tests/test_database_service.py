from database_service import get_books
from library import app
from flask import request
from werkzeug.datastructures import ImmutableMultiDict
import flask_sqlalchemy


def test_get_books_with_filter_is_base_query():
    req_content = ImmutableMultiDict([('title', 'lalka'),
                                      ('search', 'filter')])
    with app.test_request_context(
            '/', data=req_content):
        request.args = req_content
        test_results = get_books(request)

    assert isinstance(test_results, flask_sqlalchemy.BaseQuery)


def test_get_books_with_filter():
    req_content = ImmutableMultiDict([('title', 'lalka'),
                                      ('search', 'filter')])
    with app.test_request_context(
            '/', data=req_content):
        request.args = req_content
        test_results = get_books(request)

    assert isinstance(test_results, flask_sqlalchemy.BaseQuery)


def test_get_books_with_search_is_base_query():
    req_content = ImmutableMultiDict([('title', 'lalka'),
                                      ('search', 'search')])
    with app.test_request_context(
            '/', data=req_content):
        request.args = req_content
        test_results = get_books(request)

    assert isinstance(test_results, flask_sqlalchemy.BaseQuery)


def test_get_books_without_filters_is_base_query():
    with app.test_request_context('/'):
        test_results = get_books(request)
    assert isinstance(test_results, flask_sqlalchemy.BaseQuery)