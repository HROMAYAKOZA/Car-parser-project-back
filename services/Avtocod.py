import unicodedata

from bs4 import BeautifulSoup
import requests
from requests import Response

def create_html(url: str) -> Response:
    html_code = requests.get(url)
    # print("-------------------------------------------------------\n"
    #       "Connection status : {}\n".format(html_code.status_code))
    return html_code


def get_info(url: str) -> list:
    soup = BeautifulSoup(create_html(url).text, "html.parser")
    allCars = soup.findAll('div', class_="cars-list__card cars-list__card--hoverable")
    info = []
    for car in allCars:
        try:
            name = car.find('div', class_="card-car-long__desc").find('a').text
            name = name.split(' ')
            brand = name[0]
            model = ''.join(e for e in name[1] if e.isalnum())

            yearkm = car.find("div", class_="card-car-long__info-items").find_all(class_="card-car-long__info-item card-car-long__info-item--no-adaptive card-car-long__info-item--semibold")
            c = ''
            for gan in yearkm:
                c += gan.text + " "
            c = c.split()
            year = c[0]
            km = "{}{} {}".format(c[2], c[3], c[4])

            motorr = car.findAll("span", class_="card-car-long__info-item card-car-long__info-item--color-grey")
            z = ''
            for gin in motorr:
                z += gin.text + " "
            z = z.strip()
            z = z.split("/")
            if "\n" in z[2]:
                z[2] = z[2].replace("\n", "")
            z[2] = z[2].strip().split()
            z[0] = z[0].strip()
            z[1] = z[1].strip()
            m = z[2]
            motor = "{} {}, {}".format(z[0], z[1], m[0])
            if "привод" in z[2]:
                wd = "{} {}".format(m[1], m[2])
                if "дв." in z[3]:
                    transmission = "Нет информации"
                else:
                    transmission = z[3].strip()
            else:
                wd = "Нет информации"
                transmission = m[1].strip()

            href = car.find("div", class_="card-car-long").find("a").get("href").strip()
            price = unicodedata.normalize("NFKD", "{}₽".format(car
                                                               .find('span', class_="card-car-long__price")
                                                               .text))
            price = ''.join(e for e in price if e.isalnum())
            city = car.find('span', class_="card-car-long__seller-city").text
            if ' ' in city:
                city = city.split(' ')[0]
            info.append([brand, model, year, price, city, motor, transmission, wd, km, href])
        except:
            pass
    # print(info)
    return info

