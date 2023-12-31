from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
import os
from dotenv import load_dotenv
import time

load_dotenv()
postgresql_password = os.getenv("POSTGRES_PASSWORD")
host_name = os.getenv("HOST_NAME")
secret_key = os.getenv("SECRET_KEY")
app = Flask(__name__)
CORS(app)
app.secret_key = secret_key
app.app_context().push()
# time.sleep(15) # wait for PSQL start
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@{}:5432/carParser' \
    .format(postgresql_password, host_name)
db = SQLAlchemy(app)
manager = LoginManager(app)
scheduler = APScheduler()

from services import models

with app.app_context():
    db.create_all()

from services import routes
