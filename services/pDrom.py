import unicodedata

from bs4 import BeautifulSoup
import requests
from requests import Response


def create_html(url: str) -> Response:
    """This function creates the **html code** of the page"""
    html_code = requests.get(url)
    return html_code


def get_infoDrom(url: str) -> list:
    """This function returns a list of all the site's ads **drom.ru**"""
    soup = BeautifulSoup(create_html(url).text, "html.parser")
    allCars = soup.findAll('a', class_="css-xb5nz8 e1huvdhj1")
    info = []
    for car in allCars:
        try:
            name = car.find('div', class_="css-1wgtb37 e3f4v4l2").find('span').text
            name = name.split(' ')
            brand = name[0]
            model = ''.join(e for e in name[1] if e.isalnum())
            year = name[2]
            specifications = car.find("div", class_="css-1fe6w6s e162wx9x0").find_all("span")
            components = ""

            for parameter in specifications:
                components += parameter.text + " "
            components = components.split(',')
            motor = "{},{}".format(components[0], components[1])
            trs = components[2].strip().split(" ")
            transmission = ""
            if len(trs) >= 2:
                transmission += trs[1]
            else:
                transmission += trs[0]
            wd = components[3].strip()
            km = components[4].strip()

            href = car.get("href").strip()
            price = unicodedata.normalize("NFKD", "{}₽".format(car
                                                               .find('span', class_="css-46itwz e162wx9x0")
                                                               .find('span')
                                                               .text))
            price = ''.join(e for e in price if e.isalnum())
            city = str(car.find('div', class_="css-1x4jcds eotelyr0").find('span').text)
            if ' ' in city:
                city = city.split(' ')[0]

            img_url = car.find("img").get("data-src")
            info.append([brand, model, year, price, city, motor, transmission, wd, km, href, img_url])
        except:
            print("Error with connection \"{}\"".format(url))
    return info
