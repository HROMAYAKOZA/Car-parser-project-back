from flask_login import UserMixin

from services import db, manager


# class Advertisement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     brand = db.Column(db.String(128), nullable=False)
#     model = db.Column(db.String(128), nullable=False)
#     transmission = db.Column(db.String(128), nullable=False)
#     drive = db.Column(db.String(128), nullable=False)
#     body_type = db.Column(db.String(128), nullable=False)
#     color = db.Column(db.String(128), nullable=False)
#     price = db.Column(db.String(128), nullable=False)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(128), nullable=False)

    def __init__(self, brand, models):
        self.brand = brand.strip()
        self.models = [
            Model(model=model.strip()) for model in models.split(',')
        ]


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('models', lazy=True))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False)
    login = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
