from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
app = Flask(__name__, template_folder='client/templates')
app.config.from_object('app.server.config')
csrf.init_app(app)

from app.server.main import views
