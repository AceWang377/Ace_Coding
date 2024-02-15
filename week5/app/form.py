from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, TelField, TextAreaField, DecimalField, RadioField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, NumberRange, ValidationError, Email
from datetime import date
from app.model import Student,Loan

class AbbForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                    Regexp(r'^\w+$', message='Username must contain only letters, numbers, or underscores')
])
    password = PasswordField('Password', validators=[DataRequired(),
                    Length(min=4, max=12, message='Field must be included more than 4 characters and less than 12 characters'),
                    Regexp(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W_]).{8,}$',
           message='Password must be at least 8 characters long and include letters, numbers, and special characters')
])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='The two password fields did not match')])

    email_address = EmailField('Email Address', validators=[DataRequired(),
                    Length(min=6, max=15, message='Field must be between 6 and 15'),
                    Regexp(r'^\S+@\S+\.\S+$', message='Invalid email address') # validate email address
])
    date_of_birthday = DateField('Date of Birthday',validators=[DataRequired()])
    tel_phone = TelField('Telphone', validators=[DataRequired(),
                    Regexp(r'^\+?1?\d{9,15}$', message="Invalid phone number format.")
])
    location_address = TextAreaField('Address', validators=[DataRequired()])
    height = DecimalField('Height(cm)', validators=[DataRequired(), NumberRange(min=140,max=211,message='Field must be between 140cm and 211cm')])
    weight = DecimalField('Weight(kg)', validators=[DataRequired(), NumberRange(min=3,max=300,message='Field must be between 3kg and 300kg')])
    submit = SubmitField('Sign In')
    # 如果写成validate_加上form名称就会被自动调用执行
    def validate_date_of_birthday(form, field):
        if field.data > date.today():
            raise ValidationError('Date cannot be greater than today')

class MyForm(FlaskForm):
    my_field = StringField('MyABB', validators=[
        Length(min=1, max=5, message="Field must be exactly 5 characters"),
        Regexp('^[A-Za-z]+$', message="Field must contain only letters")
    ])
    submit = SubmitField('Search')

class SubjectForm(FlaskForm):
    subject_one = SelectField('First Subject',
            choices=["Biology","Chemistry","Economics","Geography","History","English","Business","Math"],
            validators=[DataRequired()])
    subject_two = SelectField('Second Subject',
            choices=["Biology","Chemistry","Economics","Geography","History","English","Business","Math"],
            validators=[DataRequired()
])
    subject_three = SelectField('Three Subject',
            choices=["Biology","Chemistry","Economics","Geography","History","English","Business","Math"],
            validators=[DataRequired(),
])
    grade_one = SelectField('Subject Grade',choices=["A","B","C","D","E","F"], validators=[DataRequired()])
    grade_two = SelectField('Subject Grade',choices=["A","B","C","D","F"], validators=[DataRequired()])
    grade_three = SelectField('Subject Grade',choices=["A","B","C","D","F"], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_subject_one(self, field):
        subjects = [self.subject_one.data, self.subject_two.data, self.subject_three.data]
        if len(subjects) != len(set(subjects)):
            raise ValidationError("Subjects must be different.")
    def validate_subject_two(self, field):
        subjects = [self.subject_one.data, self.subject_two.data, self.subject_three.data]
        if len(subjects) != len(set(subjects)):
            raise ValidationError("Subjects must be different.")
    def validate_subject_three(self, field):
        subjects = [self.subject_one.data, self.subject_two.data, self.subject_three.data]
        if len(subjects) != len(set(subjects)):
            raise ValidationError("Subjects must be different.")


class EventForm(FlaskForm):
    event_name = SelectField('Event Name',
    choices=["Forbidden City","Potala Palace","The Imperial Mountain Resort","Shenyang Imperial Palace","Confucian Temple"])
    submit = SubmitField('Submit')

class AddStudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('Firstname')
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Student')

    def validate_username(self, username):
        if Student.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already taken. Please choose another')

    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already registered. Please choose another')

class BorrowsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    borrow_devices = SelectField('Device', validators=[DataRequired()])
    submit = SubmitField('Search')

class ReturnForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    device_name = SelectField('Device', validators=[DataRequired()])
    submit = SubmitField('Confirm return')

class DeleteInfoForm(FlaskForm):
    delete_username = StringField('Delete Username', validators=[DataRequired()])
    submit = SubmitField('Confirm Delete')


class ReportForm(FlaskForm):
    reportinfo = RadioField('Report Info', choices= [('Student_ID', 'Student ID'), ('Device_ID', 'Device ID')] , validators = [DataRequired()])
    id_entered = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Request Report')