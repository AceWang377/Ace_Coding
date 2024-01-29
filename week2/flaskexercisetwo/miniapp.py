from flask import render_template,Flask,request,redirect,url_for,flash
from random import randint
from form import AbbForm,MyForm

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


if __name__ == '__main__':
    app.run(debug=True,port=5003)