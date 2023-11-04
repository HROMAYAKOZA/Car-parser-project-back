import unicodedata

from bs4 import BeautifulSoup
import requests
from requests import Response
from urllib.parse import unquote

def udal(k: list) -> list:
    for z in range(len(k)):
        if '\n' in k[z]:
            k[z] = k[z].replace('\n', '')
        if '\xa0' in k[z]:
            k[z] = k[z].replace('\xa0', '')
        if '\t' in k[z]:
            k[z] = k[z].replace('\t', '')
    return k

def create_html(url: str) -> Response:
    html_code = requests.get(url)
    return html_code


def get_info(url: str) -> list:
    soup = BeautifulSoup(create_html(url).text, "html.parser")
    allCars = soup.findAll('article', class_="catalog__item catalog__item--vertical grid__col-3")
    info = []
    for car in allCars:
        try:
            name = car.find('div', class_="catalog__info").find('span', class_="catalog__title").text
            name = name.strip().split(" ")
            brand = name[0]
            model = name[1]
            year = car.find('div', class_="catalog__info").find('span', class_="catalog__year").text.strip()
            specifications = car.findAll("li", class_="catalog__tech-item")
            components = ""

            for parameter in specifications:
                components += parameter.text + " "
            components = components.split(' ')
            udal(components)
            motor = "{} {} {} {}, {}".format(components[0], components[1], components[4], components[5], components[7])
            transmission = components[6].strip()
            wd = components[10].strip()
            km = "{} {}".format(components[2], components[3])


            href = car.find("a").get("href")
            href = "https://autograd-m.ru" + href
            price = unicodedata.normalize("NFKD", "{}₽".format(car
                                                               .find('div', class_="catalog__price")
                                                               .text))
            price = ''.join(e for e in price if e.isalnum())
            city = "Москва"
            info.append([brand, model, year, price, city, motor, transmission, wd, km, href])
        except:
            pass
    # print(info)
    return info

