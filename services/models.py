from flask_login import UserMixin

from services import db, manager


class Advertisement(db.Model):
    """This class is an advertisement table"""
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(128), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    year = db.Column(db.String(128), nullable=False)
    price = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    motor = db.Column(db.String(128), nullable=False)
    transmission = db.Column(db.String(128), nullable=False)
    wd = db.Column(db.String(128), nullable=False)
    km = db.Column(db.String(128), nullable=False)
    href = db.Column(db.String(256), nullable=False)
    img_url = db.Column(db.String(256), nullable=False)


class UserAd(db.Model):
    __tablename__ = 'user_ad'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('advertisement.id'),
                      primary_key=True)


class Users(db.Model, UserMixin):
    """This class is a users table"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False)
    login = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)


@manager.user_loader
def load_user(user_id):
    """Initializer of the user table"""
    return Users.query.get(user_id)
