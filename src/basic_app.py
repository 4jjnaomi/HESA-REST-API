from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}! Welcome to the HE Environmental Data Visualisation Board."


with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello', name="Naomi"))