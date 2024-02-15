from flask import render_template,Flask,request,redirect,url_for,flash
from random import randint
from app.form import AbbForm,MyForm,SubjectForm,EventForm,AddStudentForm,BorrowsForm,ReturnForm,DeleteInfoForm,ReportForm
from app import app,db
from app.model import Student,Loan,Device
from datetime import datetime



@app.route('/index')
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/quotes')
def quotes():
    with open('app/data/quotes.txt') as file:
        lines = file.readlines()
        length = len(lines)
        result = lines[randint(0,length-1)]
    return render_template('quotes.html',results=result)


from math import isqrt
def divisor(num):
    ever_list = []
    for i in range(1,isqrt(int(num))+1):
        if int(num) % i == 0:
            ever_list.append(i)
            ever_list.append(int(num)//i)
    return sorted(ever_list)

@app.route('/prime',methods=["POST","GET"])
def prime():
    if request.method == "POST":
        nums = request.form["num"]
        return redirect(url_for("pri_ref",nu=nums))
    else:
        return render_template("primedivisors.html")

@app.route('/prime/<nu>')
def pri_ref(nu):
    return render_template("indexone.html",primedivisors_list=divisor(nu))


@app.route('/header')
def header():
    fina_list = []
    with open('app/data/en-abbreviations.txt') as file:
        lines = file.readlines()
        for each in lines:
            if '#' not in each:
                fina_list.append(each)
    flash(f"Header found: {len(fina_list)}",category="success")

    return render_template("header.html",fina_list=fina_list)

@app.route('/search',methods=["POST","GET"])
def search():
    formabbs = MyForm()
    if formabbs.validate_on_submit():
        mydata = formabbs.my_field.data

        return redirect(url_for('pri_searches',wordsss=mydata))
    return render_template('search.html',formabb=formabbs)

@app.route('/search/<wordsss>')
def pri_searches(wordsss):
    fina_list = []
    with open('app/data/en-abbreviations.txt') as file:
        lines = file.readlines()
        for each in lines:
            if '#' not in each:
                fina_list.append(each)
    flash(f'Search for {wordsss}', 'success')
    return render_template('search_result.html',wordletter=wordsss,fina_list=fina_list)

@app.route('/login',methods=["POST","GET"])
def login():
    myloginform = AbbForm()
    if myloginform.validate_on_submit():
        username = myloginform.username.data
        flash(f'Logged in as {username}', 'success')
        return render_template('loginsuccessful.html',username=username)
    return render_template("login.html",myloginforms=myloginform)

@app.route('/grade',methods=['POST','GET'])
def gradehomepage():
    subject_form = SubjectForm()
    grade_form = SubjectForm()
    if subject_form.validate_on_submit() and grade_form.validate_on_submit():
        grade_first = grade_form.grade_one.data
        grade_second = grade_form.grade_two.data
        grade_third = grade_form.grade_three.data
        score_all = grade_first + "," +grade_second + "," + grade_third
        return redirect(url_for('gradepage',gradethree=score_all))

    return render_template('gradehomepage.html',subject_form=subject_form,grade_form=grade_form)

@app.route('/grade/<gradethree>')
def gradepage(gradethree):
    count = 0
    for each in gradethree:
        if each == 'A':
            count += 1
    if count == 3:
        flash(f'Congratulate! You got {gradethree}', 'success')
        return render_template('grade_successful.html')
    else:
        flash(f'Sorry, you got {gradethree}',category='error')
        return render_template("grade_false.html")

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

@app.route('/venue',methods=['GET','POST'])
def venuehomepage():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event_names = event_form.event_name.data
        flash(f'Your event is {event_names}', 'success')
        return redirect(url_for('venuespage',venue=event_names))
    return render_template('venueshomepage.html',event_form=event_form)


@app.route('/venue/<venue>')
def venuespage(venue):
    finally_list = []
    if venue in dic:
        value = dic[venue]
        flash(f"Congratulate! {venue} have found!",'success')
        for each in value:
            eachline = each.split(';')
            finally_list.append(eachline)
            # print(eachline)
        return render_template('events_result.html',value=finally_list)
    else:
        # flash(f'Sorry, we don not have {venue} venues','error')
        return redirect(url_for('venuehomepage'))


# exercise5
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
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            app.logger.error('Error occurred while adding student: %s', str(e))
            flash(str(e), 'danger')
            # flash('Something went wrong', 'danger')
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    borrowform = BorrowsForm()
    active_device = Device.query.all()

    borrowform.borrow_devices.choices = [ (dev.device_id,dev.device_name) for dev in active_device]
    if borrowform.validate_on_submit():
        student_info = Student.query.filter_by(username=borrowform.username.data).first()
        devices_info = Device.query.filter_by(device_id=borrowform.borrow_devices.data).first()
        if not student_info or not devices_info:
            flash('Invalid student username or device ID.', 'danger')
            return render_template("borrow_devices.html",borrowform=borrowform)
                # 检查设备是否已经被借出
        device_on_loan = Loan.query.filter_by(device_id=devices_info.device_id, returndatetime=None).first()
                # 检查学生是否有未归还的设备
        student_has_loan = Loan.query.filter_by(student_id=student_info.student_id, returndatetime=None).first()

        if device_on_loan:
            flash('This device is currently on loan.', 'danger')
        elif student_has_loan:
            flash('This student has not returned a previously borrowed device.', 'danger')
        else:
                # 处理借阅 loan
            new_loan = Loan(device_id=devices_info.device_id, student_id=student_info.student_id,
                                borrowdatetime=datetime.utcnow(), returndatetime=None)
            devices_info.is_active = False
            db.session.add(new_loan)
            db.session.add(devices_info)
            try:
                print('Committing changes to the database')
                db.session.commit()
                updated_device = Device.query.filter_by(device_id=devices_info.device_id).first()
                print('Device active status after commit:', updated_device.is_active)
                flash(f'Student {student_info.username} successfully borrowed device {devices_info.device_name}.',
                              'success')
                return redirect(url_for('home'))  # after loaning the devices and return to home page
            except Exception as e:
                db.session.rollback()
                app.logger.error('Error occurred while borrowing devices: %s', str(e))
                flash('An error occurred. Please try again.', 'danger')

    return render_template("borrow_devices.html", borrowform=borrowform)


@app.route('/return', methods=["GET", "POST"])
def returned():
    return_form = ReturnForm()
    deviceall = Device.query.all()
    return_form.device_name.choices = [ (dev.device_id,dev.device_name) for dev in deviceall]
    if return_form.validate_on_submit():
        student_names = return_form.username.data
        device_id = return_form.device_name.data
        devices_info = Device.query.filter_by(device_id=device_id).first()

        if devices_info and devices_info.is_active is False:
            # create a return logic
            record_loan = Loan.query.filter_by(device_id=device_id,returndatetime=None).first()
            if record_loan:
                record_loan.returndatetime = datetime.utcnow()
                devices_info.is_active = True
                db.session.add(devices_info)
                db.session.add(record_loan)
                db.session.commit()
                flash(f'Student {student_names} have returned device {devices_info.device_name}','success')

            else:
                flash(f'No outstanding loan record found for this device.','warning')
        else:
            flash(f'the device {device_id} is not currently on loan!','info')
        return redirect(url_for('home'))
    return render_template("return_device.html",return_form=return_form)


@app.route('/deleteinfo', methods=["GET", "POST"])
def deleteinfo():
    delete_form = DeleteInfoForm()
    if delete_form.validate_on_submit():
        deletename = delete_form.delete_username.data
        deleteuser = Student.query.filter_by(username=deletename).first()
        if deleteuser:
            db.session.delete(deleteuser)
            db.session.commit()
            flash(f'Student {deletename} have been deleted','success')
        else:
            flash(f'Student {deletename} is not in the student database','info')

        return redirect(url_for('home'))
    return render_template('deletestudent.html',delete_form=delete_form)

@app.route('/requestinfo', methods=["GET", "POST"])
def requestinfo():
    request_form = ReportForm()
    if request_form.validate_on_submit():
        choosen = request_form.reportinfo.data
        idinfo = request_form.id_entered.data
        if choosen == 'Student_ID':
            student_info = Student.query.filter_by(student_id=idinfo).first()
            if student_info:
                loan_info = Loan.query.filter_by(student_id=idinfo).all()
            else:
                loan_info = None
            if not student_info:
                flash('Student {idinfo} is not in the student database','warning')
            return render_template('report_result.html', student_info=student_info, loan_info=loan_info)
        elif choosen == 'Device_ID':
            device_info = Device.query.filter_by(device_id=idinfo).first()
            if device_info:
                loan_info = Loan.query.filter_by(device_id=idinfo).first()
            else:
                loan_info = None
            if not device_info:
                flash('Device {idinfo} is not in the device database','warning')
            return render_template('report_result.html',device_info=device_info,loan_info=loan_info)
    return render_template('report_info.html',request_form=request_form)
