from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class AbbForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class MyForm(FlaskForm):
    my_field = StringField('MyABB', validators=[
        Length(min=1, max=5, message="Field must be exactly 5 characters"),
        Regexp('^[A-Za-z]+$', message="Field must contain only letters")
    ])
    submit = SubmitField('Search')

