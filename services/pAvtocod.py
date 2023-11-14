import unicodedata
from bs4 import BeautifulSoup
import re
from services.pDrom import create_html, real_trans


def get_infoAvtocod(url: str) -> list:
    """This function returns a list of all the site's ads **cars.avtocod.ru**"""
    soup = BeautifulSoup(create_html(url).text, "html.parser")
    allCars = soup.findAll('div',
                           class_="cars-list__card cars-list__card--hoverable")
    info = []
    for car in allCars:
        try:
            name = car.find('div', class_="card-car-long__desc").find('a').text
            name = name.split(' ')
            brand = name[0]
            model = ''.join(e for e in name[1] if e.isalnum())

            year_km = car.find("div",
                               class_="card-car-long__info-items").find_all(
                class_="card-car-long__info-item card-car-long__info-item--no"
                       "-adaptive card-car-long__info-item--semibold")
            c = ''
            for gan in year_km:
                c += gan.text + " "
            params = c.split()
            year = params[0]
            km = "{}{} {}".format(params[2], params[3], params[4])

            HTML_motor = car.findAll("span",
                                     class_="card-car-long__info-item "
                                            "card-car-long__info-item--color"
                                            "-grey")
            z_str = ''
            for gin in HTML_motor:
                z_str += gin.text + " "
            z = z_str.strip().split("/")
            if "\n" in z[2]:
                z[2].replace("\n", "").strip()
            trans = z[2].split()
            z[0].strip()
            z[1].strip()
            m = trans.copy()
            motor = ("{} {}, {}".format(z[0], z[1], m[0])).lower()
            if "привод" in trans:
                wd = "{} {}".format(m[1], m[2])
                if "дв." in z[3]:
                    transmission = "Нет информации"
                else:
                    transmission = z[3].strip()
            else:
                wd = "Нет информации"
                transmission = m[1].strip()
            transmission = real_trans(transmission)

            href = car.find("div", class_="card-car-long").find("a").get(
                "href").strip()
            price = unicodedata \
                .normalize("NFKD", "{}₽"
                           .format(car.find('span',
                                            class_="card-car-long__price")
                                   .text))
            price = ''.join(e for e in price if e.isalnum())
            city = car.find('span', class_="card-car-long__seller-city").text
            if ' ' in city:
                city = city.split(' ')[0]
            img_url = car.find("a").find('img').get('src')
            if re.findall(r"https://adsboard-static.spectrumdata", img_url):
                if transmission != "нет информации" and wd != "нет информации":
                    info.append(
                        [brand, model, year, price, city, motor, transmission,
                         wd, km, href, img_url])
        except:
            print("Error with connection \"{}\"".format(url))
    # print(info)
    return info
