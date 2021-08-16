from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DateField
from wtforms.validators import InputRequired, URL, Optional, Length


class BookForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('author', validators=[InputRequired()])
    published_date = DateField('Published date', validators=[
        InputRequired()])
    ISBN = IntegerField('ISBN', validators=[InputRequired()])
    num_pages = IntegerField('Pages', validators=[InputRequired()])
    cover_url = TextAreaField("Link to the cover", validators=[
        Optional(), URL(message="Enter Valid URL Please.")])
    language = StringField('Language', validators=[InputRequired()])

    def validate_ISBN(form, field):
        original_ISBN = form.data['ISBN']
        try:
            ISBN = str(original_ISBN)
            if len(ISBN) == 10 or len(ISBN) == 13:
                pass
            else:
                message = f"A valid ISBN number is comprised of 10 or 13 digits. Currently {ISBN}"
                raise ValidationError(message)
        except AttributeError:
            raise ValidationError(f"Not a valid number {original_ISBN}")
