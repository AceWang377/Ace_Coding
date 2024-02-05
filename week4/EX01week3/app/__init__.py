from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] =  b'WR#&f&+%78er0we=%799eww+#7^90-;s'

from app import views