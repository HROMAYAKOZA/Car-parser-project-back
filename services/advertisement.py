from bs4 import BeautifulSoup
from requests import Response
from sqlalchemy import Integer
from services.models import Advertisement
from services.pDrom import create_html, get_infoDrom
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
    """This function **selects the database fields** that match the input data"""
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


def insert_ad_from_drom(city_list, hmta) -> None:
    """This function **adds ads with drom.ru** to the database using the function  *pDrom.py/get_infoDrom()*
    \n(called once when the server starts)"""
    for city in city_list:
        count = 0
        for url in city:
            ads = get_infoDrom(url)
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


def get_statusDS_drom(html: Response) -> BeautifulSoup:
    """This is the function of **checking the ad for relevance**"""
    soup = BeautifulSoup(html.text, "html.parser")
    status = soup.find("div", class_="e1jb3i2p0 css-14asbju e1u9wqx22")
    return status


def updatingADS() -> None:
    """This function **removes** out-of-date ads and **replaces** them with up-to-date ones"""
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
