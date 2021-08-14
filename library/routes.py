from flask import render_template, request, redirect, url_for, flash
from library import app, db
from library.models import Book
from library.forms import BookForm


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
        'form.html', form=form, errors=errors, entry_id=book_id)


@app.route('/', methods=['GET'])
def homepage():
    filters = {key: value for key, value in request.args.items() if value}
    if filters:
        books = Book.query.filter_by(**filters).order_by(
            Book.author.asc())
    else:
        books = Book.query.all() #order_by(Book.author.asc())
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
