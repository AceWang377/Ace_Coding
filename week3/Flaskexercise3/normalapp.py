from flask import render_template,Flask,request,redirect,url_for,flash
from random import randint
from form import AbbForm,MyForm,SubjectForm,EventForm

app = Flask(__name__)
app.config['SECRET_KEY'] =  b'WR#&f&+%78er0we=%799eww+#7^90-;s'

@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quotes')
def quotes():
    with open('data/quotes.txt') as file:
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
    with open('data/en-abbreviations.txt') as file:
        lines = file.readlines()
        for each in lines:
            if '#' not in each:
                fina_list.append(each)

    return render_template("header.html",fina_list=fina_list)

@app.route('/search',methods=["POST","GET"])
def search():
    formabbs = MyForm()
    if formabbs.validate_on_submit():
        mydata = formabbs.my_field.data
        flash(f'Search for {mydata}', 'success')
        return redirect(url_for('pri_searches',wordsss=mydata))
    return render_template('search.html',formabb=formabbs)

@app.route('/search/<wordsss>')
def pri_searches(wordsss):
    fina_list = []
    with open('data/en-abbreviations.txt') as file:
        lines = file.readlines()
        for each in lines:
            if '#' not in each:
                fina_list.append(each)

    return render_template('search_result.html',wordletter=wordsss,fina_list=fina_list)

@app.route('/login',methods=["POST","GET"])
def login():
    myloginform = AbbForm()
    if myloginform.validate_on_submit():
        username = myloginform.username.data
        password = myloginform.password.data
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
        flash(f'Sorry, we don not have {venue} venues','error')
        return redirect(url_for('venuehomepage'))

if __name__ == '__main__':
    app.run(debug=True,port=5001)