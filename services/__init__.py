from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from services.settings import postgresql_password, secret_key

app = Flask(__name__)
app.secret_key = secret_key
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@localhost/carParser'.format(postgresql_password)
db = SQLAlchemy(app)
manager = LoginManager(app)

from services import routes, models

db.create_all()

app.run(debug=True)
