from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/<name>')
def hello(name):
    return f'Hello {name}!'


@app.route('/')
def home():
    return redirect(url_for('hello', name='World'))


if __name__ == '__main__':
    app.run()
