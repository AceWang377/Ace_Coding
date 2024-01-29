# exercise one -- Show the date and time of day when the user lands on the home page of the app
'''
from flask import Flask,render_template
from datetime import datetime
app = Flask(__name__)

@app.route('/')

def templates():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run(debug=True,port=5001)
'''

'''

# exercise two -- print from the quotes
from flask import Flask,render_template
import random
app = Flask(__name__)

@app.route('/')

def templates():
    with open("./static/quotes") as file:
        lines = file.readlines()
    return lines[random.randint(0,len(lines))]

if __name__ == '__main__':
    app.run(debug=True,port=5001)
'''
'''
# exercise 3 -- Write an app that uses a dynamic route ending with a positive integer and generates a page that shows
# the prime divisors of the integer (which may be just 1 and the integer itself if it is prime). You can use
# code from the web for primality testing (c.f.Primality_test)
from math import isqrt
def divisor(num):
    ever_list = []
    for i in range(1,isqrt(int(num))+1):
        if int(num) % i == 0:
            ever_list.append(i)
            ever_list.append(int(num)//i)
    return sorted(ever_list)

from flask import Flask,render_template
app = Flask(__name__)
@app.route('/<num>')
def dynamic(num):
    return render_template('indexone.html',primedivisors_list=divisor(num))
if __name__ == '__main__':
    app.run(debug=True,port=5001)
'''
'''
# exercise 4 -- Write an app that shows values from the App object on one page and the Request object on another
from flask import Flask,render_template,request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/app')
def oneobject():
    app_info = {
        'Development': app.config['DEBUG'],
        'Testing': app.config['TESTING'],
        'App Name': app.name,
        'Instance Path': app.instance_path
    }
    return render_template('indextwo.html',app_info=app_info)

@app.route('/request')
def anotherobject():
    request_info = {
        'URL': request.url,
        'Method': request.method,
        'Headers': request.headers
    }
    return render_template('indexthree.html',request_info=request_info)

if __name__ == "__main__":
    app.run(debug=True,port=5001)
'''

# exercise 5
from random import randint
from datetime import datetime
from flask import Flask,render_template,redirect,request,url_for
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/datetime')
def date():
    clock = datetime.now()
    return render_template("datetime.html",clockssss=clock)

@app.route('/quotes')
def quo():
    with open("static/quotes") as file:
        lines = file.readlines()
    return lines[randint(0,len(lines))]

from math import isqrt
def divisor(num):
    ever_list = []
    for i in range(1,isqrt(int(num))+1):
        if int(num) % i == 0:
            ever_list.append(i)
            ever_list.append(int(num)//i)
    return sorted(ever_list)
@app.route('/prime',methods=["POST","GET"])
def pri():
    if request.method == "POST":
        nums = request.form["num"]
        return redirect(url_for("pri_ref",nu=nums))
    else:
        return render_template("prime.html")

@app.route('/prime/<nu>')
def pri_ref(nu):
    return render_template("indexone.html",primedivisors_list=divisor(nu))

@app.route('/app')
def oneobject():
    app_info = {
        'Development': app.config['DEBUG'],
        'Testing': app.config['TESTING'],
        'App Name': app.name,
        'Instance Path': app.instance_path
    }
    return render_template('indextwo.html',app_info=app_info)

@app.route('/request')
def anotherobject():
    request_info = {
        'URL': request.url,
        'Method': request.method,
        'Headers': request.headers
    }
    return render_template('indexthree.html',request_info=request_info)

if __name__ == '__main__':
    app.run(debug=True,port=5002)


