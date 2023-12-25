from __future__ import annotations

from typing import Any

from flask import request, jsonify, Response
from werkzeug.security import check_password_hash, generate_password_hash

from services import app, db
from services.models import Users, Advertisement, UserAd
from services.href import cities
from services.advertisement import sorted_selectFromADS, \
    insert_ad_to_Advertisement
from services.users import changeParOfUser, selectAdsOfUser

if not Advertisement.query.first():
    insert_ad_to_Advertisement(cities, 10)
cities_db = []
brands = []
models = []
transmissions = []
models.append("All")
transmissions.append("All")
for ad in Advertisement.query.all():
    if not (ad.city in cities_db):
        cities_db.append(ad.city)
    if not (ad.brand in brands):
        brands.append(ad.brand)
    if not (ad.model in models):
        models.append(ad.model)
    if not (ad.transmission in transmissions):
        transmissions.append(ad.transmission)

InfoLists = {"cities": cities_db, "brands": brands,
             "models": models, "transmissions": transmissions}


@app.route('/', methods=['GET', 'POST'])
def main():
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
        ads = sorted_selectFromADS(brand, model, city, price_from,
                                   price_to, year, trans)
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


@app.route('/selectFavoriteAds/<UserID>', methods=['GET', 'POST'])
def selectFavoriteAds(UserID):
    query = UserAd.query.filter_by(user_id=UserID).all()
    favoriteAds = []
    for i in query:
        favoriteAds.append(i.ad_id)
    return jsonify({'favoriteAds': favoriteAds})


@app.route('/selectFavoriteAdsALL/<UserID>', methods=['GET', 'POST'])
def selectFavoriteAdsALL(UserID):
    query = UserAd.query.filter_by(user_id=UserID).all()
    Ads = []
    for i in query:
        Ads.append(Advertisement.query.filter_by(id=i.ad_id).first())
    favoriteAds = [{'id': item.id,
                    'brand': item.brand,
                    'model': item.model,
                    'year': item.year,
                    'price': item.price,
                    'href': item.href,
                    'image': item.img_url} for item in Ads]

    return jsonify({'favoriteAds': favoriteAds})


@app.route('/setAdInUser/<UserID>/<AdID>', methods=['GET'])
def setAdInUser(UserID, AdID):
    flag = UserAd.query.filter_by(user_id=UserID, ad_id=AdID).first()
    if not flag:
        newAd = UserAd(user_id=UserID, ad_id=AdID)
        db.session.add(newAd)
        db.session.commit()

    return {'result': 'Successfully'}


@app.route('/deleteAdOfUser/<UserID>/<AdID>', methods=['GET'])
def deleteAdOfUser(UserID, AdID):
    pair = UserAd.query.filter_by(user_id=UserID, ad_id=AdID).first()
    if pair:
        db.session.delete(pair)
        db.session.commit()
    return {'result': 'Successfully'}


@app.route('/login', methods=['POST', 'GET'])
def login_page() -> dict:
    """Returns a dictionary with an error message and the username of the user.
    If the error message is empty in the dictionary,then the user is
    transferred to his account"""
    result = {'message': '', 'nickname': ''}
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = Users.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            result['login'] = login
            result['nickname'] = user.nickname
            result['id'] = user.id
            return result
        else:
            result['message'] = "Неверный логин или пароль"
    else:
        result['message'] = "Пожалуйста, введите логин и пароль"
    return result


@app.route('/registration', methods=['POST', 'GET'])
def registration() -> dict:
    """Returns a dictionary with an error message and the username
    of the user. If the error message is empty in the dictionary,
    then the user is successfully registered"""
    result = {'message': '', 'nickname': ''}
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
                result['nickname'] = nickname
                hash_password = generate_password_hash(password)
                newUser = Users(nickname=nickname, login=login,
                                password=hash_password)
                db.session.add(newUser)
                db.session.commit()

    return result


@app.route('/account/<userID>', methods=['GET'])
def user_page(userID) -> Response | dict[str, Any]:
    """Returns a dictionary in which the key is a parameter**, and the
    value is a list from which you can select a variant of this
    parameter"""
    user = Users.query.filter_by(id=userID).first()
    favorites = selectAdsOfUser(userID)
    result = {'nickname': user.nickname, 'favorites': favorites}
    return jsonify(result)


@app.route('/account/<userID>/changeParams', methods=['GET', 'POST'])
def userChangeParams(userID):
    nickname = request.form.get('newName')
    login = request.form.get('newLogin')
    result = changeParOfUser(userID, nickname, login)
    return jsonify(result)
