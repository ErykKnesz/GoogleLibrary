from flask import (render_template, request, redirect, url_for, flash,
                   jsonify, abort, make_response)
from library import app, db
from library.models import Book
from library.forms import BookForm
import google_api_client as gsf
import database_service as ds


def add_or_edit_book(book_id, book, form):
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit() and book_id:
            form.populate_obj(book)
            db.session.commit()
            return redirect(url_for('homepage'))
        elif form.validate_on_submit():
            db.session.add(book)
            db.session.commit()
            flash("Yeah, thanks!", 'success')
        else:
            errors = form.errors
            flash(f"Oops... See the following errors: {errors}", 'danger')
    return render_template(
        'form.html', form=form, errors=errors, book_id=book_id)


@app.route('/', methods=['GET'])
def homepage():
    books = ds.get_books(request)
    if isinstance(books, list):
        books.sort(key=lambda x: x.author)
    else:
        books.order_by(Book.author.asc())
    return render_template('homepage.html', books=books)


@app.route("/add-book", methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    book_id = None
    book = Book(
        title=form.title.data,
        author=form.author.data,
        published_date=form.published_date.data,
        ISBN=form.ISBN.data,
        num_pages=form.num_pages.data,
        cover_url=form.cover_url.data,
        language=form.language.data
        )
    return add_or_edit_book(book_id, book, form)


@app.route("/edit-book/<int:book_id>", methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id).first_or_404()
    form = BookForm(obj=book)
    return add_or_edit_book(book_id, book, form)


@app.route("/search-google-api", methods=['GET'])
def search_google_api():
    search_query = request.args
    if search_query:
        results = gsf.search(search_query)
        if results:
            gsf.results_to_db(results)
            return redirect(url_for('homepage'))
    return render_template('google_search_form.html',
                           search_query=search_query)


@app.route("/api/v1/books", methods=['GET'])
def get_expenses():
    allowed_filters = ['title', 'author', 'published_date', 'ISBN',
                       'num_pages', 'cover_url', 'language']
    for filter in request.args.keys():
        if filter not in allowed_filters:
            abort(400)
    books = ds.get_books(request)
    books = list(books)
    for index, book in enumerate(books):
        books[index] = {
            'title': book.title,
            'author': book.author,
            'published date': book.published_date.strftime('%Y-%m-%d'),
            'ISBN': book.ISBN,
            'page count': book.num_pages,
            'cover url': book.cover_url,
            'language': book.language
        }
    return jsonify(books)


@app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify({'error': 'Bad request', 'status_code': 400}), 400
    )
