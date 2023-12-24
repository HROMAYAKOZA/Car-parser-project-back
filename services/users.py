from werkzeug.security import check_password_hash, generate_password_hash

from services import db
from services.models import Users, UserAd, Advertisement


def selectAdsOfUser(userID):
    """Returns all the user's favorite ads"""
    UA_query = UserAd.query.filter(UserAd.user_id == userID).all()
    favorites = []
    for item in UA_query:
        advert = Advertisement.query.filter(
            Advertisement.id == item.ad_id).first()
        temp = {'id': advert.id, 'price': advert.price,
                'brand': advert.brand, 'model': advert.model,
                'year': advert.year, 'km': advert.km, 'image': advert.img_url,
                'motor': advert.motor, 'transmission': advert.transmission,
                'wd': advert.wd, 'href': advert.href}

        favorites.append(temp)
    return favorites


def changeParOfUser(userID, nickname, login):
    """Changes the user's login and nickname"""
    result = {'message': ""}
    user = Users.query.filter_by(id=userID).first()
    if not nickname:
        nickname = user.nickname
    if not login:
        login = user.login
    else:
        if ' ' in list(login):
            result['message'] = "Логин не должен содержать пробела"
        else:
            user = Users.query.filter_by(login=login).first()
            if user:
                result['message'] = "Этот логин уже занят"
    if result['message'] == "":
        mainUser = Users.query.filter_by(id=userID).first()
        mainUser.nickname = nickname
        mainUser.login = login

        db.session.commit()
    return result
