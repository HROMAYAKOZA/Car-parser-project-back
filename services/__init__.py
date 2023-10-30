from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from services.settings import postgresql_password, secret_key, host_name
import time

# Sleep for 30 seconds
time.sleep(30)

app = Flask(__name__)
CORS(app)
app.secret_key = secret_key
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@{}:5432/carParser'.format(postgresql_password, host_name)
db = SQLAlchemy(app)
manager = LoginManager(app)
scheduler = APScheduler()

from services import models, routes
with app.app_context():
    db.create_all()
