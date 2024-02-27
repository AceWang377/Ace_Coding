
from flask import render_template, url_for, flash, redirect
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, BorrowForm, ReturnForm, RemoveForm, ReportForm, \
    SubjectForm, VenusForm, LoanForm, LoanDeleteForm
from app.forms import AddBankAccountForm, TransactionForm
from app.models import Student, Loan, User, BankAccount, Transaction


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
        if User.query.filter_by(username=form.username.data).first():
            flash(f'Username {form.username} have already been registered', 'danger')
        if User.query.filter_by(email=form.email.data).first():
            flash(f'Email {form.email} have already been used', 'danger')

        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'Registration for {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            # app.logger.error(e)
            flash('Something went wrong', 'danger')
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

        if not student:
            flash(f'Student with id {student_id} does not exist', 'danger')
        if Loan.query.filter_by(device_id=device_id, returndatetime=None).first():
            flash(f'Device with id {device_id} does not return', 'danger')
        if Loan.query.filter_by(student_id=student_id, returndatetime=None).first():
            flash(f'Student with id {student_id} does not return device', 'danger')
        if student.is_active == True:
            new_loan = Loan(device_id=device_id,
                            student_id=student_id,
                            borrowdatetime=datetime.utcnow(),
                            returndatetime=None)
            student.is_active = False
            db.session.add(new_loan)
            try:
                db.session.commit()
                flash(f'New Loan added', 'success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash(f'Could not add new loan', 'warning')
        else:
            flash(f'Student with id {student_id} is not active', 'warning')
    return render_template('borrow.html', title='Borrow', form=form)


@app.route('/return', methods=['GET', 'POST'])
def return_page():
    form = ReturnForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        device_id = form.device_id.data
        student = Student.query.filter_by(student_id=student_id).first()
        return_Loan = Loan.query.filter_by(student_id=student_id,device_id=device_id,returndatetime=None).first()

        if return_Loan:
            return_Loan.returndatetime = datetime.utcnow()
            student.is_active = True
            db.session.add(return_Loan)
            try:
                db.session.commit()
                flash(f'Returned Loan', 'success')
                return redirect(url_for('index'))
            except:
                flash(f'Could not return device', 'warning')

        elif not return_Loan:
            flash(f'Student {student_id} does not borrow any books or device {device_id} does not be borrowed','warning')

    return render_template('return.html', form=form)


@app.route('/remove', methods=['GET', 'POST'])
def remove_student():
    form = RemoveForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        remove_student = Student.query.filter_by(student_id=student_id).first()
        record_loan = Loan.query.filter_by(student_id=student_id).first()
        # 删除借贷记录后 再删除学生信息 必须删除数据库之间相互关联的数据
        # for loan in record_loan:
        #     db.session.delete(loan)
        #     db.session.commit()
        if record_loan.returndatetime == None:
            flash(f'Student {student_id} has loan recorded, Please return the device {record_loan.device_id}', 'danger')
            return redirect(url_for('return_page'))
        elif record_loan.returndatetime != None and remove_student:
            db.session.delete(record_loan)
            db.session.delete(remove_student)
            db.session.commit()
            flash(f'Student {student_id} have been removed','success')
            return redirect(url_for('index'))
        elif record_loan.returndatetime != None and not remove_student:
            flash(f'Student {student_id} does not in the database','warning')
    return render_template('remove_student.html',form=form)


@app.route('/report', methods=['GET', 'POST'])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        choice = form.report_name.data
        value = form.report_id.data
        if choice == 'Student_id':
            student = Student.query.filter_by(student_id=value).first()
            if student:
                loan_record = Loan.query.filter_by(student_id=value).all()
            else:
                flash(f'Student {value} does not exist','danger')
                loan_record = None
            return render_template("report_result.html",student=student, loan_record=loan_record)
        elif choice == 'Device_id':
            loan_record = Loan.query.filter_by(device_id=value).all()
            if not loan_record:
                flash(f'Device {value} does not have loan record','warning')

            return render_template("report_result.html",loan_record=loan_record)

    return render_template('report_form.html', form=form)


@app.route('/grade', methods=['GET', 'POST'])
def grade():
    form = SubjectForm()

    if form.validate_on_submit():
        grade_one = form.grade_one.data
        grade_two = form.grade_two.data
        grade_three = form.grade_three.data
        grade_all = grade_one + grade_two + grade_three
        return redirect(url_for('grade_page', gra = grade_all))

    return render_template("grade_page.html",form=form)

@app.route('/grade/<gra>')
def grade_page(gra):
    count = 0
    for each in gra:
        if each == 'A':
            count += 1
    if count == 3:
        flash(f'{gra} You have right to apply cs subject now!','success')
    else:
        flash(f'{gra} You can not apply cs subject now!','warning')
    return redirect(url_for('index'))

dic = {
    "Forbidden City":["The Avenue;12.2.2024",
                "Paradise Gardens;11.2.2024",
                "Atlantis;3.11.2024",
                "The Blue Fin;4.13.2024",
                "The Greenhouse;5.12.2024",
                "Big Orchid;7.11.2024"],
    "Potala Palace":["Lotus Lakes;4.23.2024",
                    "The Golden Plaza;9.25.2024",
                    "Omni;10.30.2024",
                    "Prime Lands;11.11.2024"],
    "The Imperial Mountain Resort":["The Quaint Cottages;2.28.2024",
                    "La Parisienne;2.09.2024",
                    "Anette’s Place;9.21.2024"],
    "Shenyang Imperial Palace":["The Arctic;10.1.2024",
                    "Mirage;7.8.2024",
                    "Harbor Town;10.24.2024",
                    "Sapphire Palace;6.22.2024"],
    "Confucian Temple":["Nebula;11.2.2024",
                    "Enchanted Venues;2.23.2024",
                    "Casa Nicolette;3.12.2024",
                    "Marianne’s Events Place;7.9.2024"]
}

@app.route('/venus',methods=['GET','POST'])
def venus():
    form = VenusForm()
    if form.validate_on_submit():
        search_word = form.address.data.lower()
        for keys,vals in dic.items():
            if search_word in keys.lower():
                show_words = ",".join(vals)
                break
        if show_words:
            return redirect(url_for('venus_page', search_word=show_words))
    return render_template('venus.html',form=form)

@app.route('/venus/<search_word>')
def venus_page(search_word):
    fina_list = search_word.split(',')
    return render_template('venus_page.html',search_word=fina_list)



@app.route('/add_bankaccount',methods=['GET','POST'])
def add_bankaccount():
    form = AddBankAccountForm()
    if form.validate_on_submit():
        bank_name = form.bank_name.data
        account_deposit = form.account_deposit.data
        user_id = form.user_id.data
        if User.query.filter_by(user_id=user_id).first():
            new_bankaccount = BankAccount(bank_name=bank_name,account_deposit=account_deposit,user_id=user_id)
            db.session.add(new_bankaccount)
            try:
                db.session.commit()
                flash(f'Bank Account user {user_id} has been added.','success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error occur while adding bank account %s',str(e))
                flash(str(e),'danger')
        else:
            flash(f'user {user_id} does not exist.','danger')
    return render_template("add_bank_account.html",form=form)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    form = TransactionForm()
    if form.validate_on_submit():
        bank_id = form.bank_account_id.data
        object_id = form.object_bank_id.data
        transactions_type = form.transaction_type.data
        amount_value = form.transaction_amount.data
        # query.get(). 获取table中的某一个信息 只能是Primary key才可以使用get
        current_amount = BankAccount.query.get(bank_id).account_deposit
        if BankAccount.query.filter_by(bank_account_id=bank_id).first() is None:
            # 在用户完成输入后整体提示输入的银行账户问题
            # flash(f'Bank Account {bank_id} does not exist.','warning')
            # 在输入完成后及时反馈是否存在问题
            form.bank_account_id.errors.append('Bank Account does not exist.','danger')
        if BankAccount.query.filter_by(bank_account_id=object_id).first() is None:
            # flash(f'Bank Account {object_id} does not exist.','warning')
            form.bank_account_id.errors.append('Bank Account does not exist.','danger')
        if bank_id != object_id:
            if transactions_type == 'withdraw_money':
                if current_amount > amount_value:
                    amount = current_amount - amount_value
                    new_transaction = Transaction(bank_id=bank_id,object_id=object_id,
                                                  account_withdraw=amount_value,
                                                  account_deposit=0,transaction_date=datetime.utcnow())
                    db.session.add(new_transaction)
                    BankAccount.query.filter_by(bank_account_id=bank_id).update({'account_deposit': amount})
                    try:
                        db.session.commit()
                        flash(f'Transaction {transactions_type} was successfully','success')

                        return redirect(url_for('index'))
                    except:
                        db.session.rollback()
                        flash(f'Transaction {transactions_type} was unsuccessfully','danger')
                else:
                    flash(f'Your Bank Account does not have enough money.','danger')
            elif transactions_type == 'deposit_money':
                amount = current_amount + amount_value
                new_transaction = Transaction(bank_id=bank_id,object_id=object_id,
                                              account_withdraw=0,
                                              account_deposit=amount_value,
                                              transaction_date=datetime.utcnow())
                db.session.add(new_transaction)
                BankAccount.query.filter_by(bank_account_id=bank_id).update({'account_deposit': amount})
                try:
                    db.session.commit()
                    flash(f'Transaction {transactions_type} was successfully','success')
                    return redirect(url_for('index'))
                except:
                    db.session.rollback()
                    flash('Transaction {transactions_type} was unsuccessfully','danger')

        else:
            flash(f'You can not do transaction {transactions_type} with yourself','danger')
            return redirect(url_for('transactions'))


    return render_template('transaction_form.html',form=form)


@app.route('/student_list',methods=['GET','POST'])
def student_list():
    studentList = Student.query.filter_by().first()
    return render_template('student_list.html',studentList=studentList)

@app.route('/loan',methods=['GET','POST'])
def loan_page():
    form = LoanForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        device_id = form.device_id.data
        student = Student.query.get(student_id)
        active = Student.query.filter_by(student_id=student_id).first()

        if not student:
            flash(f'Student {student_id} does not exist','danger')

        if Loan.query.filter_by(student_id=student_id,returndatetime=None).first():
            flash(f'Student {student_id} has not return device','warning')

        if Loan.query.filter_by(device_id=device_id,returndatetime=None).first():
            flash(f'Device {device_id} has not return','warning')


        if active.is_active == True:
            new_loan = Loan(student_id=student_id
                            ,device_id=device_id,
                            borrowdatetime=datetime.utcnow(),
                            returndatetime=None)
            active.is_active = False
            db.session.add(new_loan)
            try:
                db.session.commit()
                flash(f'Student {student_id} loan was successfully','success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash(f'Student {student_id} loan was unsuccessfully','danger')

        else:
            flash(f'Student {student_id} is not active','warning')

    return render_template('loan_page.html',form=form)


@app.route('/loan_return',methods=['GET','POST'])
def loan_return():
    form = ReturnForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        device_id = form.device_id.data
        student = Student.query.filter_by(student_id=student_id).first()
        student_loan_record = Loan.query.filter_by(student_id=student_id).first()

        if student_loan_record is None:
            flash(f'Student {student_id} has not loan record','warning')
        if Loan.query.filter_by(device_id=device_id,returndatetime=None).first() is None:
            flash(f'Device {device_id} has not been loaned','warning')
        if Loan.query.filter_by(student_id=student_id,device_id=device_id,returndatetime=None).first():
            Loan.query.filter_by(student_id=student_id,device_id=device_id,returndatetime=None).update({'returndatetime':datetime.utcnow()})
            student.is_active = True
            db.session.add(student)
            try:
                db.session.commit()
                flash(f'Student {student_id} has returned device','success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'something went wrong {str(e)}','danger')
                return redirect(url_for('loan_return'))

    return render_template('loan_return.html',form=form)


@app.route('/loan_delete/',methods=['GET','POST'])
def loan_delete():
    form = LoanDeleteForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        loan_record = Loan.query.filter_by(student_id=student_id).all()
        if loan_record is not None:
            if Loan.query.filter_by(student_id=student_id,returndatetime=None).first():
                flash(f'Student {student_id} has been loaned a device and has not returned, Please return the device first.','warning')
                return redirect(url_for('loan_return'))
            else:
                Loan.query.filter_by(student_id=student_id).delete()
                db.session.commit()
                flash(f'Student {student_id} loan record has been deleted','success')
                return redirect(url_for('index'))
        else:
            flash(f'Student {student_id} does not has any loan record','warning')
    return render_template('loan_delete.html',form=form)

@app.route('/remove/',methods=['GET','POST'])
def remove():
    form = RemoveForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        student = Student.query.filter_by(student_id=student_id).first()
        if Loan.query.filter_by(student_id=student_id,returndatetime=None).first():
            flash(f'Student {student_id} has been loaned a device and has not returned','warning')
            return redirect(url_for('loan_return'))
        if student:
            if Loan.query.filter_by(student_id=student_id).all():
                Loan.query.filter_by(student_id=student_id).delete()
            Student.query.filter_by(student_id=student_id).delete()
            try:
                db.session.commit()
                flash(f'Student {student_id} has been removed','success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash(f'Student {student_id} has not been deleted','warning')
        else:
            flash(f'Student {student_id} is not exists','warning')
            return redirect(url_for('remove'))

    return render_template('remove_student.html',form=form)

