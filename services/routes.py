from flask import render_template, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user
from services import app, db
from services.models import Users, Advertisement
from services.href import cities
from services.advertisement import sorted_selectFromADS, \
    insert_ad_to_Advertisement

# insert_ad_to_Advertisement(cities, 10)
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


@app.route('/advertisement/<ID>', methods=['GET', 'POST'])
def car_page(ID):
    advert = Advertisement.query.filter(Advertisement.id == ID).first()
    return render_template("oneCarInfo.html", ad=advert)


@app.route('/login', methods=['POST', 'GET'])
def login_page() -> dict:
    """Returns a dictionary with an error message and the username of the user.\n
     If the error message is empty in the dictionary,then the user is transferred to his account"""
    result = {'message': '', 'username': ''}
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = Users.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            print("login")
            result['username'] = current_user.nickname
            return result
        else:
            result['message'] = "Неверный логин или пароль"
    else:
        result['message'] = "Пожалуйста, введите логин и пароль"
    print("Login: {0}  {1}".format(login, password))
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
                newUser = Users(nickname=nickname, login=login,
                                password=hash_password)
                db.session.add(newUser)
                db.session.commit()

    print("{2} : {0}  {1}".format(login, password, nickname))
    return result


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


# @app.after_request
# def redirect_to_signin(response):
#     if response.status_code == 401:
#         return redirect(url_for('login_page') + '?next=' + request.url)
#     return response


# @app.route('/account/<username>', methods=['GET'])
# @login_required
# def user_page(username):
#     return render_template('account.html')

@app.route('/account', methods=['GET'])
def user_page() -> dict:
    """Returns a dictionary in which the **key is a parameter**,
    and the **value is a list** from which you can select a variant of this parameter"""
    name = current_user.nickname
    info = {"username": name}
    return info
