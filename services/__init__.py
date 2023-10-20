from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from settings import postgresql_password, secret_key


app = Flask(__name__)
app.secret_key = secret_key
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@localhost/carParser'.format(postgresql_password)
db = SQLAlchemy(app)
manager = LoginManager(app)
scheduler = APScheduler()

with app.app_context():
    db.create_all()
