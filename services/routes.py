from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user
from services import app, db
from services.models import Users, Advertisement
from services.advertisement import sorted_selectFromADS


@app.route('/', methods=['GET', 'POST'])
def main() -> str:
    return ""


@app.route('/login', methods=['POST', 'GET'])
def login_page() -> dict:
    """Returns a dictionary with an **error message** and the **username** of the user.\n
     If the error message **is empty** in the dictionary,then the user is **transferred to his account**"""
    result = {'message': '', 'username': ''}
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = Users.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            result['username'] = current_user.nickname
        else:
            result['message'] = "Неверный логин или пароль"
    else:
        result['message'] = "Пожалуйста, введите логин и пароль"
    print("{0}  {1}".format(login, password))
    return result


@app.route('/registration', methods=['POST', 'GET'])
def registration() -> dict:
    """Returns a **dictionary** with an **error message** and the **username** of the user.\n
    If the error message **is empty** in the dictionary, then the user is **successfully registered**"""
    result = {'message': '', 'username': ''}
    nickname = request.form.get('nickname')
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if not (password or password2 or login or nickname):
        result['message'] = "Пожалуйста, заполните все поля"
    elif password != password2:
        result['message'] = "Пароли не совпадают"
    else:
        if ' ' in list(login):
            result['message'] = "Логин не должен содержать пробела"
        else:
            user = Users.query.filter_by(login=login).first()
            if user:
                result['message'] = "Этот логин уже занят"
            else:
                result['username'] = nickname
                hash_password = generate_password_hash(password)
                newUser = Users(nickname=nickname, login=login, password=hash_password)
                db.session.add(newUser)
                db.session.commit()

    print("{2} : {0}  {1}".format(login, password, nickname))
    return result



@app.route('/account', methods=['GET', 'POST'])
def user_page() -> dict:
    """Returns a dictionary in which the **key is a parameter**,
    and the **value is a list** from which you can select a variant of this parameter"""
    name = current_user.nickname
    cities = []
    brands = []
    models = []
    for ad in Advertisement.query.all():
        if not (ad.city in cities):
            cities.append(ad.city)
        if not (ad.brand in brands):
            brands.append(ad.brand)
        if not (ad.model in models):
            models.append(ad.model)
    info = {"name": name, "brands": brands, "models": models, "cities": cities}
    return info


@app.route('/search_car', methods=['POST'])
def search_car() -> list:
    """This function processes **all parameters** entered by the user
     and **outputs information corresponding to these parameters**"""
    brand = request.form.get('brand')
    model = request.form.get('model')
    city = request.form.get('city')
    price_from = request.form.get('price_from')
    price_to = request.form.get('price_to')
    ads = sorted_selectFromADS(brand, model, city, price_from, price_to)
    return ads
