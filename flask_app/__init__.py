from flask import Flask
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
app.secret_key = "flubbernuggets"
Bootstrap5(app)