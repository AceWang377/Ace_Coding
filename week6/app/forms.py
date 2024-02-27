from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField, SelectField,SearchField
from wtforms.fields.datetime import DateTimeField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Student, Loan
from sqlalchemy import and_


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


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


class BorrowForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Borrow Device')

    def validate_student_id(self, student_id):
        if not student_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if not Student.query.get(student_id.data):
            raise ValidationError('There is no student with this id in the system')
        if Loan.query.filter(
                    (Loan.student_id == student_id.data)
                    &
                    # (Loan.returndatetime.is_(None))
                    (Loan.returndatetime.is_(None))
                ).first():
            raise ValidationError('This student cannot borrow another item until the previous loan has been returned')

    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if Loan.query.filter(
                    (Loan.device_id == device_id.data)
                    &
                    (Loan.returndatetime.is_(None))
                ).first():
            raise ValidationError('This device cannot be borrowed as it is currently on loan')


class ReturnForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Return')

    def validate_student_id(self, student_id):
        if not student_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if not Student.query.get(student_id.data):
            raise ValidationError('There is no student with this id in the system')


    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')


class RemoveForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Remove Student')


class ReportForm(FlaskForm):
    report_name = RadioField('Report Name', choices=[("Student_id","Student_id"),("Device_id","Device_id")],validators=[DataRequired()])
    report_id = StringField('Report ID', validators=[DataRequired()])
    submit = SubmitField('Report')

class SubjectForm(FlaskForm):
    subject_one = SelectField('Subject Name', choices=["Biology","Chemistry","Economics","Geography","History","English","Business","Math"],validators=[DataRequired()])
    subject_two = SelectField('Subject Name',
                              choices=["Biology", "Chemistry", "Economics", "Geography", "History", "English",
                                       "Business", "Math"], validators=[DataRequired()])
    subject_three = SelectField('Subject Name',
                              choices=["Biology", "Chemistry", "Economics", "Geography", "History", "English",
                                       "Business", "Math"], validators=[DataRequired()])
    grade_one = SelectField('Grade', choices=["A","B","C"],validators=[DataRequired()])
    grade_two = SelectField('Grade', choices=["A", "B", "C"], validators=[DataRequired()])
    grade_three = SelectField('Grade', choices=["A", "B", "C"], validators=[DataRequired()])
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

class VenusForm(FlaskForm):
    address = SearchField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddBankAccountForm(FlaskForm):
    bank_name = StringField('Bank Name', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    account_deposit = IntegerField('Bank Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TransactionForm(FlaskForm):
    bank_account_id = StringField('Bank Account', validators=[DataRequired()])
    object_bank_id = StringField('Transaction Bank ID', validators=[DataRequired()])
    transaction_type = RadioField('Transaction Type', choices=[('withdraw_money', 'Withdraw Money'),
                                                               ('deposit_money','Deposit Money')],
                                 validators=[DataRequired()])
    transaction_amount = IntegerField('Transaction Amount', validators=[DataRequired()])
    submit = SubmitField('Transaction')


class LoanForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    device_id = IntegerField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Loan')

class LoanDeleteForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Loan')