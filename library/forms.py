from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, URL, Optional


class BookForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('author', validators=[InputRequired()])
    published_date = StringField('Published year', validators=[InputRequired()])
    ISBN = IntegerField('ISBN', validators=[InputRequired()])
    num_pages = IntegerField('Pages', validators=[InputRequired()])
    cover_url = TextAreaField("Link to the cover", validators=[Optional(), URL()])
    language = StringField('Language', validators=[InputRequired()])