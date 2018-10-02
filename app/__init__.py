from flask import Flask
from flask_wtf.csrf import CSRFProtect
import requests_cache

app = Flask(__name__, template_folder='client/templates')

app.config.from_object('app.server.config')
if app.config['CSRF_ENABLED'] is True:
    csrf = CSRFProtect()
    csrf.init_app(app)

# Cache expires after 180 seconds
requests_cache.install_cache(cache_name='cache', backend='sqlite', expire_after=180)

from app.server.main import views
