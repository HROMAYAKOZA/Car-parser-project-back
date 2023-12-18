from __future__ import annotations

from typing import Any

from flask import request, jsonify, \
    session, Response
from werkzeug.security import check_password_hash, generate_password_hash

from services import app, db
from services.models import Users, Advertisement
from services.href import cities
from services.advertisement import sorted_selectFromADS, \
    insert_ad_to_Advertisement

if not Advertisement.query.first():
    insert_ad_to_Advertisement(cities, 10)
cities_db = []
brands = []
models = []
years = []
transmissions = []
for ad in Advertisement.query.all():
    if not (ad.city in cities_db):
        cities_db.append(ad.city)
    if not (ad.brand in brands):
        brands.append(ad.brand)
    if not (ad.model in models):
        models.append(ad.model)
    if not (ad.year in years):
        years.append(ad.year)
    if not (ad.transmission in transmissions):
        transmissions.append(ad.transmission)

InfoLists = {"cities": cities_db, "brands": brands, "models": models,
             "years": years, "transmissions": transmissions}


@app.route('/', methods=['GET', 'POST'])
def main():
    print(session.get('logged_in'))
    if session.get('logged_in'):
        InfoLists["auth"] = "TRUE"
    else:
        InfoLists["auth"] = "FALSE"
    if request.method == 'GET':
        ads = Advertisement.query.limit(11).all()
        InfoLists["ads"] = [{'id': item.id,
                             'brand': item.brand,
                             'model': item.model,
                             'year': item.year,
                             'price': item.price,
                             'href': item.href,
                             'image': item.img_url} for item in ads]
        return jsonify(InfoLists)
    elif request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        city = request.form.get('city')
        year = request.form.get('year')
        trans = request.form.get('transmission')
        price_from = request.form.get('price_from')
        price_to = request.form.get('price_to')
        ads = sorted_selectFromADS(brand, model, city,
                                   price_from, price_to)
        InfoLists["ads"] = [{'id': item.id,
                             'brand': item.brand,
                             'model': item.model,
                             'year': item.year,
                             'price': item.price,
                             'href': item.href,
                             'image': item.img_url} for item in ads]
        return jsonify(InfoLists)


@app.route('/advertisement/<ID>', methods=['GET'])
def car_page(ID):
    advert = Advertisement.query.filter(Advertisement.id == ID).first()
    result = {'id': advert.id,
              'price': advert.price,
              'brand': advert.brand,
              'model': advert.model,
              'year': advert.year,
              'km': advert.km,
              'motor': advert.motor,
              'transmission': advert.transmission,
              'wd': advert.wd,
              'href': advert.href,
              'image': advert.img_url}
    return jsonify(result)


@app.route('/login', methods=['POST', 'GET'])
def login_page() -> dict:
    """Returns a dictionary with an error message and the username of the
    user.\n If the error message is empty in the dictionary,then the user is
    transferred to his account"""
    result = {'message': '', 'username': ''}
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = Users.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = login
            session.permanent = True

            result['username'] = login
            return result
        else:
            result['message'] = "Неверный логин или пароль"
    else:
        result['message'] = "Пожалуйста, введите логин и пароль"
    print("Login: {0}  {1}".format(login, password))
    return result


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)

    return jsonify({'message': 'Logout successful'}), 200


@app.route('/registration', methods=['POST', 'GET'])
def registration() -> dict:
    """Returns a **dictionary** with an **error message** and the
    **username** of the user.\n If the error message **is empty** in the
    dictionary, then the user is **successfully registered**"""
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
                newUser = Users(nickname=nickname, login=login,
                                password=hash_password)
                db.session.add(newUser)
                db.session.commit()

    return result


@app.route('/account', methods=['GET'])
def user_page() -> Response | dict[str, Any]:
    """Returns a dictionary in which the **key is a parameter**, and the
    **value is a list** from which you can select a variant of this
    parameter"""
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'})

    info = {"username": session.get('username'), "message": ""}
    return jsonify(info)
