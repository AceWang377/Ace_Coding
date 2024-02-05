from flask import render_template, redirect, url_for, flash
from app import app
from datetime import datetime
from app.forms import LoginForm, RegistrationForm

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
