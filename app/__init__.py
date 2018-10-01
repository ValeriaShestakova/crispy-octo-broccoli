from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='client/templates')
app.config.from_object('app.server.config')
if app.config['CSRF_ENABLED'] is True:
    csrf = CSRFProtect()
    csrf.init_app(app)

from app.server.main import views
