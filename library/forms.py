from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, TextAreaField,
                     DateField, HiddenField)
from wtforms.validators import InputRequired, URL, Optional
from library.models import Book


def unique_check(form, field):
    filter = {field.name: field.data}
    book = Book.query.filter_by(**filter).first()
    if book:
        if book.id == form.id.data:
            message = f"This {field.name} '{field.data}' " \
                      f"already exists in the database"
            raise ValidationError(message)


class BookForm(FlaskForm):
    id = HiddenField('id')
    title = StringField('Title', validators=[InputRequired(), unique_check])
    authors = StringField('authors', validators=[InputRequired()])
    published_date = DateField('Published date', validators=[
        InputRequired()])
    ISBN = StringField('ISBN', validators=[InputRequired(), unique_check])
    num_pages = IntegerField('Pages', validators=[InputRequired()])
    cover_url = TextAreaField("Link to the cover", validators=[
        Optional(), URL(message="Enter Valid URL Please.")])
    language = StringField('Language', validators=[InputRequired()])

    def validate_ISBN(form, field):
        original_isbn = field.data
        try:
            isbn = len(original_isbn)
            if isbn == 10 or isbn == 13:
                pass
            else:
                message = f"A valid ISBN number is comprised of " \
                          f"10 or 13 digits. Currently {isbn}"
                raise ValidationError(message)
        except AttributeError:
            raise ValidationError(f"Not a valid number {original_isbn}")

    def validate_language(form, field):
        lang = field.data
        if len(lang) != 2:
            message = "Please use 2-letter language codes, e.g 'en' " \
                      "as per the standard ISO 639-1"
            raise ValidationError(message)


def enlist_errors(form_errors: dict):
    errors = ""
    for k, v in form_errors.items():
        error = "- " + k + ": " + str(v).strip('[]') + ",\n"
        errors += error
    return errors