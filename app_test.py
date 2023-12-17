import pytest
from services import app
from services.pDrom import get_infoDrom
from services.pAvtocod import get_infoAvtocod
from services.pAutograd import get_infoAutograd

def test_parsers():
    assert get_infoDrom("https://moscow.drom.ru/toyota/camry/page1/") != []
    assert get_infoAvtocod("https://cars.avtocod.ru/avto-s-probegom/ford/")!=[]
    assert get_infoAutograd("https://autograd-m.ru/cars/hummer")!=[]

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_routes(client):   
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hummer' in response.data

def test_registration_login(client):
    response = client.post('/registration', data={'nickname': 'test_nickname','login':'test_login','password':'1234','password2':'1234'})
    assert response.status_code == 200
    assert response.data == b'{"message":"","username":"test_nickname"}\n'
    response = client.post('/login', data={'login':'test_login','password':'1234'})
    assert response.status_code == 200
    assert response.data == b'{"message":"","username":"test_login"}\n'