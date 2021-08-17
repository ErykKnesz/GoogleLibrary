from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DateField
from wtforms.validators import InputRequired, URL, Optional
from library.models import Book


def unique_check(form, field):
    filter = {field.name: field.data}
    if Book.query.filter_by(**filter).first():
        message = f"This {field.name} '{field.data}' " \
                  f"already exists in the database"
        raise ValidationError(message)


class BookForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), unique_check])
    author = StringField('author', validators=[InputRequired()])
    published_date = DateField('Published date', validators=[
        InputRequired()])
    ISBN = IntegerField('ISBN', validators=[InputRequired(), unique_check])
    num_pages = IntegerField('Pages', validators=[InputRequired()])
    cover_url = TextAreaField("Link to the cover", validators=[
        Optional(), URL(message="Enter Valid URL Please.")])
    language = StringField('Language', validators=[InputRequired()])

    def validate_ISBN(form, field):
        original_isbn = field.data
        try:
            isbn = len(str(original_isbn))
            if isbn == 10 or isbn == 13:
                pass
            else:
                message = f"A valid ISBN number is comprised of 10 or 13 digits. Currently {isbn}"
                raise ValidationError(message)
        except AttributeError:
            raise ValidationError(f"Not a valid number {original_isbn}")


