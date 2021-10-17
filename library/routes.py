from flask import (render_template, request, redirect, url_for, flash,
                   jsonify, abort, make_response)
from library import app, db
from library.models import Book
from library.forms import BookForm, enlist_errors
import google_api_client as gac
import database_service as ds


def add_or_edit_book(book, form, book_id=None):
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit() and book_id:
            form.authors.data = ds.preprocess_form_authors(form)
            form.populate_obj(book)
            db.session.commit()
            return redirect(url_for('homepage'))
        elif form.validate_on_submit():
            db.session.add(book)
            authors = ds.preprocess_form_authors(form)
            for author in authors:
                book.authors.append(author)
            db.session.commit()
            flash("Yeah, thanks!", 'success')
        else:
            errors = enlist_errors(form.errors)
            flash(f"Oops... See the following errors: {errors}", 'danger')
    return render_template(
        'form.html', form=form, errors=errors, book_id=book_id, book=book)


@app.route('/api/v1/books', methods=['GET'])
def get_books():
    allowed_filters = ['title', 'authors', 'min date', 'max date', 'ISBN',
                       'num_pages', 'cover_url', 'language', 'search']
    for filter in request.args.keys():
        if filter not in allowed_filters:
            abort(400)
    books = ds.get_books(request)
    books = list(books)
    for index, book in enumerate(books):
        authors = []
        for author in book.authors:
            authors.append(author.name)
        books[index] = {
            'title': book.title,
            'authors': authors,
            'published date': book.published_date.strftime('%Y-%m-%d'),
            'ISBN': book.ISBN,
            'page count': book.num_pages,
            'cover url': book.cover_url,
            'language': book.language
        }
    return jsonify(books)


@app.route('/', methods=['GET'])
def homepage():
    page = request.args.get('page', 1, type=int)
    books = ds.get_books(request)
    books = books.paginate(page, 10, False)
    query = request.query_string.decode()
    if 'page' in query:
        query = query.replace(f"page={page}&", "")
    return render_template('homepage.html', books=books, query=query)


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    book = Book(
        title=form.title.data,
        published_date=form.published_date.data,
        ISBN=form.ISBN.data,
        num_pages=form.num_pages.data,
        cover_url=form.cover_url.data,
        language=form.language.data
        )
    return add_or_edit_book(book, form)


@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id).first_or_404()
    form = BookForm(obj=book)
    return add_or_edit_book(book, form, book_id=book_id)


@app.route('/search-google-api', methods=['GET'])
def search_google_api():
    search_query = request.args
    if search_query:
        results = gac.search(search_query)
        if results:
            gac.results_to_db(results)
            return redirect(url_for('homepage'))
    return render_template('google_search_form.html',
                           search_query=search_query)


@app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify({'error': 'Bad request', 'status_code': 400}), 400
    )
