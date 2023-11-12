from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from services import app, db
from services.models import Users, Advertisement
from services.advertisement import sorted_selectFromADS, insert_ad_to_Advertisement
from services.href import cities

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


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        ads = Advertisement.query.all()
        return render_template('index.html',
                               ads=ads,
                               len=5, brands=brands,
                               models=models, cities=cities_db,
                               trans=transmissions, years=years)
    elif request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        city = request.form.get('city')
        year = request.form.get('year')
        trans = request.form.get('transmission')
        price_from = request.form.get('price_from')
        price_to = request.form.get('price_to')
        ads = sorted_selectFromADS(brand, model, city, price_from, price_to)
        return render_template('index.html',
                               ads=ads,
                               len=len(ads), brands=brands,
                               models=models, cities=cities_db,
                               trans=transmissions, years=years)


@app.route('/advertisement/<ID>', methods=['GET', 'POST'])
def car_page(ID):
    advert = Advertisement.query.filter(Advertisement.id == ID).first()
    return render_template("oneCarInfo.html", ad=advert)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if request.method == 'POST':
        if login and password:
            user = Users.query.filter_by(login=login).first()
            if user and check_password_hash(user.password, password):
                login_user(user)

                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for("user_page", username=current_user.nickname))
            else:
                flash("Неверный логин или пароль")

        else:
            flash("Пожалуйста, введите логин и пароль")

    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    nickname = request.form.get('nickname')
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (password or password2 or login or nickname):
            flash("Пожалуйста, заполните все поля")
        elif password != password2:
            flash("Пароли не совпадают")
        else:
            if ' ' in list(login):
                flash("Логин не должен содержать пробела")
            else:
                user = Users.query.filter_by(login=login).first()
                if user:
                    flash("Этот логин уже занят")
                else:
                    hash_password = generate_password_hash(password)
                    newUser = Users(nickname=nickname, login=login, password=hash_password)
                    db.session.add(newUser)
                    db.session.commit()

                    return redirect(url_for('login_page'))

    return render_template('registration.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


@app.route('/account/<username>', methods=['GET'])
@login_required
def user_page(username):
    return render_template('account.html')
