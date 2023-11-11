import base64

import requests
from bs4 import BeautifulSoup
from requests import Response
from sqlalchemy import Integer
import re

from services.pAutograd import get_infoAutograd
from services.pAvtocod import get_infoAvtocod
from services.models import Advertisement
from services.pDrom import create_html, get_infoDrom
from services import app, db


def sorted_selectFromADS(brand, model, city, price_from, price_to) -> list:
    """This function **selects the database fields** that match the input data"""
    ads = []
    if model != "All":
        if price_from and price_to:
            ads = Advertisement.query.filter(Advertisement.brand == brand, Advertisement.model == model,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) >= int(price_from),
                                             Advertisement.price.cast(Integer) <= int(price_to)).all()
        elif price_to and not price_from:
            ads = Advertisement.query.filter(Advertisement.brand == brand, Advertisement.model == model,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) <= int(price_to)).all()
        elif price_from and not price_to:
            ads = Advertisement.query.filter(Advertisement.brand == brand, Advertisement.model == model,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) >= int(price_from)).all()
        else:
            ads = Advertisement.query.filter(Advertisement.brand == brand, Advertisement.model == model,
                                             Advertisement.city == city).all()
    else:
        if price_from and price_to:
            ads = Advertisement.query.filter(Advertisement.brand == brand,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) >= int(price_from),
                                             Advertisement.price.cast(Integer) <= int(price_to))
        elif price_to and not price_from:
            ads = Advertisement.query.filter(Advertisement.brand == brand,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) <= int(price_to)).all()
        elif price_from and not price_to:
            ads = Advertisement.query.filter(Advertisement.brand == brand,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) >= int(price_from)).all()
        else:
            ads = Advertisement.query.filter(Advertisement.brand == brand,
                                             Advertisement.city == city).all()

    return ads


def insert_ad_to_Advertisement(city_list, hmta) -> None:
    """This function fills the **"Advertisement" table** with ads from sites **drom.ru; autograd-m.ru;
    cars.avtocod.ru**"""
    for city in city_list:
        count = 0
        for url in city:
            ads = []
            if re.findall(r".drom.ru/", url):
                ads = get_infoDrom(url)
            elif re.findall(r"https://autograd-m.ru", url):
                ads = get_infoAutograd(url)
            elif re.findall(r"https://cars.avtocod.ru", url):
                ads = get_infoAvtocod(url)
            print(ads)
            for ad in ads:
                advert = Advertisement.query.filter_by(href=ad[9]).first()
                if not advert and count < hmta:
                    newAd = Advertisement(brand=ad[0], model=ad[1], year=ad[2], price=ad[3], city=ad[4], motor=ad[5],
                                          transmission=ad[6], wd=ad[7], km=ad[8], href=ad[9], img_url=ad[10])
                    db.session.add(newAd)
                    db.session.commit()
                    count += 1
                else:
                    break
            count = 0
            continue


def get_statusAD(html: Response, url: str) -> BeautifulSoup:
    """This is the function of **checking the ad for relevance**"""
    soup = BeautifulSoup(html.text, "html.parser")
    if re.findall(r".drom.ru/", url):
        status = soup.find("div", class_="e1jb3i2p0 css-14asbju e1u9wqx22")
        return status
    elif re.findall(r"https://autograd-m.ru", url):
        status = soup.find("div", class_="not-found__block")
        return status
    elif re.findall(r"https://cars.avtocod.ru", url):
        status = soup.find("div", class_="wrap")
        return status


def updatingADS() -> None:
    """This function **removes** out-of-date ads and **replaces** them with up-to-date ones"""
    app.app_context().push()
    ads = Advertisement.query.all()
    for ad in ads:
        url = ad.href
        html = create_html(url)
        try:
            status = get_statusAD(html, url)
            if status is not None:
                deleteAD = Advertisement.query.filter_by(href=url).first()
                print(deleteAD.href)
                href = str(deleteAD.href)[:-13]
                print(href)
                insert_ad_to_Advertisement([href], 1)
                db.session.delete(deleteAD)
                db.session.commit()
            else:
                print("{} - is active".format(ad.id))
        except:
            db.session.delete(url)
            db.session.commit()


def get_picture(url: str):
    # Отправьте GET-запрос по указанному URL-адресу и получите содержимое страницы
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Найдите теги <img> на странице
    img = soup.find_all("img")
    img_url = img[0]["src"]
    img_response = requests.get(img_url)

    # Преобразуйте содержимое изображения в формат base64
    img_base64 = base64.b64encode(img_response.content).decode('utf-8')

    # Верните HTML-страницу с изображением
    return f'<img src="data:image/jpeg;base64,{img_base64}" alt="Image">'
