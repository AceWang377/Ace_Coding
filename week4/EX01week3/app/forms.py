from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# To enable email validation,
# 1. install the email-validation package in your py312 environment,
# 2. Comment out the following import line and uncomment the next one
# 3. follow the instructions below for the email field in the RegistrationForm Class
# from wtforms.validators import DataRequired, EqualTo
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # To enable email validation, comment out the following line and uncomment the next one:
    # email = StringField('Email', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

