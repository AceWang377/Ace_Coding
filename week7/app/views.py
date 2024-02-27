from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required,login_user,logout_user
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, BorrowForm, ReturnLoanForm
from app.models import Student, Loan


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('index'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    form = BorrowForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        device_id = form.device_id.data
        student = Student.query.filter_by(student_id=student_id).first()
        student_loan_record = Loan.query.filter_by(student_id=student_id).all()
        damaged_status_student = False
        if not student:
            flash(f'Student {student_id} is not exist', 'danger')
        if Loan.query.filter_by(student_id=student_id,returndatetime=None).first():
            flash(f'Student {student_id} has not return device', 'danger')
        if Loan.query.filter_by(device_id=device_id,returndatetime=None).first():
            flash(f'Device {device_id} has not return','warning')

        for loan_record in student_loan_record:
            if loan_record.damaged == True:
                damaged_status_student = True
        if damaged_status_student == False:
            new_loan = Loan(device_id=form.device_id.data,
                            student_id=form.student_id.data,
                            borrowdatetime=datetime.now())

            db.session.add(new_loan)
            try:
                db.session.commit()
                flash(f'New Loan added', 'success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash('Something went wrong while adding new loan', 'danger')
        else:
            flash(f'Student {student_id} has damaged record','danger')
    return render_template('borrow.html', title='Borrow', form=form)


@app.route('/list_loan', methods=['GET', 'POST'])
def list_loan():
    loans = Loan.query.filter_by().all()
    students = Student.query.filter_by().all()
    return render_template('list_loan.html', title='list loan', loans=loans, students=students)


@app.route('/return', methods=['GET', 'POST'])
def returnLoan():
    form = ReturnLoanForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        device_id = form.device_id.data
        damaged_status = form.damaged_status.data
        student = Student.query.filter_by(student_id=student_id).first()

        if student is None:
            flash(f'Student {student_id} does not in the database', 'danger')
        if Loan.query.filter_by(device_id=device_id, returndatetime=None).first() is None:
            flash(f'Device {device_id} has been borrowed', 'danger')
        if Loan.query.filter_by(student_id=student_id,device_id=device_id,returndatetime=None).first():
            Loan.query.filter_by(student_id=student_id, device_id=device_id, returndatetime=None).update(
                {'returndatetime': datetime.utcnow()})
            if damaged_status == True:
                Loan.query.filter_by(student_id=student_id, device_id=device_id).update({'damaged':True})
            try:
                db.session.commit()
                flash(f'Device {device_id} has been returned', 'success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash(f'Something went wrong, Please try again', 'danger')
        else:
            flash(f'Student {student_id} has not borrow device {device_id}', 'danger')

    return render_template('return.html', title='return loan', form=form)

