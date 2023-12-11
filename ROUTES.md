# Car-parser-project

## Routes
#### Главная страница.
```python
@app.route('/', methods=['GET', 'POST'])
def main() -> str:
    return ""
```

#### Страница входа.
```python
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    result = {'message': '', 'username': ''}
    return result
```
*Возвращает сообщение об ошибке и имя пользователя*

#### Страница регистрации.
```python
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    result = {'message': '', 'username': ''}
    return result
```
*Возвращает сообщение об ошибке и имя пользователя*

#### Страница ввода данных для парсера.
```python
@app.route('/account', methods=['GET'])
@login_required
def user_page(username):
    transmissions = ['Auto', 'Mechanics']
    cities = []
    brands = []
    models = []
    info = {"brands": brands, "models": models, "cities": cities}
    return info
```
*Возвращает **Map** где по ключам хранятся списки*

#### Страница результата парсера.
```python
@app.route('/search_car', methods=['POST'])
@login_required
def search_car():
    brand = request.form.get('brand')
    model = request.form.get('model')
    city = request.form.get('city')
    price_from = request.form.get('price_from')
    price_to = request.form.get('price_to')
    ads = sorted_selectFromADS(brand, model, city, price_from, price_to)
    return ads
```
*Возвращает результат парсера в виде двухмерного массива где один массив это одно объявление*