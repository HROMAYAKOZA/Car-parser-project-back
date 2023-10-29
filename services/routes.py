from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from services import app, db
from services.models import Users, Advertisement
from services.advertisement import sorted_selectFromADS


@app.route('/', methods=['GET', 'POST'])
def hello_world() -> str:
    return ""


@app.route('/login', methods=['POST', 'GET'])
def login_page():
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
def registration():
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


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


@app.route('/<username>', methods=['GET'])
@login_required
def user_page(username):
    transmissions = ['Auto', 'Mechanics']
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
    return render_template('account.html',
                           brands=brands,
                           models=models,
                           cities=cities)


@app.route('/search_car', methods=['POST'])
@login_required
def search_car():
    brand = request.form.get('brand')
    model = request.form.get('model')
    city = request.form.get('city')
    price_from = request.form.get('price_from')
    price_to = request.form.get('price_to')
    ads = sorted_selectFromADS(brand, model, city, price_from, price_to)
    return render_template('info.html', ads=ads)
