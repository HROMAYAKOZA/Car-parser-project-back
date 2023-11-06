from bs4 import BeautifulSoup
from requests import Response
from sqlalchemy import Integer
from services.models import Advertisement
from services.pDrom import create_html, get_info
from services import app, db

msk = ["https://moscow.drom.ru/toyota/camry/page1/", "https://moscow.drom.ru/toyota/corolla/page1/",
       "https://moscow.drom.ru/nissan/x-trail/page1/", "https://moscow.drom.ru/nissan/note/page1/",
       "https://moscow.drom.ru/honda/fit/page1/", "https://moscow.drom.ru/honda/cr-v/page1/",
       "https://moscow.drom.ru/mazda/demio/page1/", "https://moscow.drom.ru/bmw/m5/page1/",
       "https://moscow.drom.ru/bmw/m4/page1/", "https://moscow.drom.ru/mercedes-benz/s-class/page1/",
       "https://moscow.drom.ru/mercedes-benz/e-class/page1/"]
spb = ["https://spb.drom.ru/toyota/camry/page1/", "https://spb.drom.ru/toyota/corolla/page1/",
       "https://spb.drom.ru/nissan/x-trail/page1/", "https://spb.drom.ru/nissan/note/page1/",
       "https://spb.drom.ru/honda/fit/page1/", "https://spb.drom.ru/honda/cr-v/page1/",
       "https://spb.drom.ru/mazda/demio/page1/", "https://spb.drom.ru/bmw/m5/page1/",
       "https://spb.drom.ru/bmw/m4/page1/", "https://spb.drom.ru/mercedes-benz/s-class/page1/",
       "https://spb.drom.ru/mercedes-benz/e-class/page1/"]

bal = ["https://balashiha.drom.ru/toyota/camry/page1/", "https://balashiha.drom.ru/toyota/corolla/page1/",
       "https://balashiha.drom.ru/nissan/x-trail/page1/", "https://balashiha.drom.ru/nissan/note/page1/",
       "https://balashiha.drom.ru/honda/fit/page1/", "https://balashiha.drom.ru/honda/cr-v/page1/",
       "https://balashiha.drom.ru/mazda/demio/page1/", "https://balashiha.drom.ru/bmw/m5/page1/",
       "https://balashiha.drom.ru/bmw/m4/page1/", "https://balashiha.drom.ru/mercedes-benz/s-class/page1/",
       "https://balashiha.drom.ru/mercedes-benz/e-class/page1/"]

blg = ["https://blagoveshchensk.drom.ru/toyota/camry/page1/",
       "https://blagoveshchensk.drom.ru/toyota/corolla/page1/",
       "https://blagoveshchensk.drom.ru/nissan/x-trail/page1/",
       "https://blagoveshchensk.drom.ru/nissan/note/page1/",
       "https://blagoveshchensk.drom.ru/honda/fit/page1/",
       "https://blagoveshchensk.drom.ru/honda/cr-v/page1/",
       "https://blagoveshchensk.drom.ru/mazda/demio/page1/",
       "https://blagoveshchensk.drom.ru/bmw/m5/page1/",
       "https://blagoveshchensk.drom.ru/bmw/m4/page1/",
       "https://blagoveshchensk.drom.ru/mercedes-benz/s-class/page1/",
       "https://blagoveshchensk.drom.ru/mercedes-benz/e-class/page1/"]

cities = [blg, bal, msk, spb]


def sorted_selectFromADS(brand, model, city, price_from, price_to) -> list:
    ads = []
    if model != "All":
        if price_from and price_to:
            ads = Advertisement.query.filter(Advertisement.brand == brand, Advertisement.model == model,
                                             Advertisement.city == city,
                                             Advertisement.price.cast(Integer) >= int(price_from),
                                             Advertisement.price.cast(Integer) <= int(price_to))
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


def insert_ad_from_drom(city, hmta):
    count = 0
    for url in city:
        ads = get_info(url)
        for ad in ads:
            advert = Advertisement.query.filter_by(href=ad[9]).first()
            if not advert and count < hmta:
                newAd = Advertisement(brand=ad[0], model=ad[1], year=ad[2], price=ad[3], city=ad[4], motor=ad[5],
                                      transmission=ad[6], wd=ad[7], km=ad[8], href=ad[9])
                db.session.add(newAd)
                db.session.commit()
                count += 1
            else:
                break
        count = 0
        continue


def get_statusDS_drom(html: Response):
    soup = BeautifulSoup(html.text, "html.parser")
    status = soup.find("div", class_="e1jb3i2p0 css-14asbju e1u9wqx22")
    return status


def updatingADS():
    app.app_context().push()
    ads = Advertisement.query.all()
    for ad in ads:
        url = ad.href
        html = create_html(url)
        try:
            status = get_statusDS_drom(html)
            if status:
                deleteAD = Advertisement.query.filter_by(href=url).first()
                print(deleteAD.href)
                href = str(deleteAD.href)[:-13]
                print(href)
                insert_ad_from_drom([href], 1)
                db.session.delete(deleteAD)
                db.session.commit()
            else:
                print("{} - is active".format(ad.id))
        except:
            db.session.delete(url)
            db.session.commit()


def insert_tableADS(city_list: list):
    for city in city_list:
        insert_ad_from_drom(city, 3)


# insert_tableADS(cities)
