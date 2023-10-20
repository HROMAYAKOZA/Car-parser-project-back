from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from services import app, db
from services.models import Users, Advertisement
from services.advertisement import sorted_selectFromADS


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
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
        if not(ad.city in cities):
            cities.append(ad.city)
        if not(ad.brand in brands):
            brands.append(ad.brand)
        if not(ad.model in models):
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
