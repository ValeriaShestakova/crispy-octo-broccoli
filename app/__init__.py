from flask import Flask

app = Flask(__name__)

from app.server.main import views
