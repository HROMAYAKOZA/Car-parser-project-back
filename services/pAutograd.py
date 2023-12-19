import unicodedata

from bs4 import BeautifulSoup
from services.pDrom import create_html, refactoringTRM, refactoringWD


def get_infoAutograd(url: str) -> list:
    """This function returns a list of all the site's ads autograd-m.ru"""
    soup = BeautifulSoup(create_html(url).text, "html.parser")
    allCars = soup.findAll('article',
                           class_="catalog__item catalog__item--vertical grid"
                                  "__col-3")
    info = []
    for car in allCars:
        try:
            name = car.find('div', class_="catalog__info") \
                .find('span', class_="catalog__title").text
            name = name.strip().split(" ")
            brand = name[0]
            model = name[1]
            year = car.find('div', class_="catalog__info") \
                .find('span', class_="catalog__year").text.strip()
            specifications = car.findAll("li", class_="catalog__tech-item")
            components = ""

            for parameter in specifications:
                components += parameter.text + " "
            components = components.split(' ')
            for z in range(len(components)):
                components[z] = components[z] \
                    .replace('\n', '').replace('\xa0', '').replace('\t', '')

            motor = "{} {} {} {}, {}".format(components[0], components[1],
                                             components[4], components[5],
                                             components[7].lower())
            transmission = components[6].strip()
            transmission = refactoringTRM(transmission)
            wd = components[10].strip()
            wd = refactoringWD(wd)
            km = "{} {}".format(components[2], components[3])

            href = car.find("a").get("href")
            href = "https://autograd-m.ru" + href
            price = unicodedata \
                .normalize("NFKD", "{}₽"
                           .format(car.find('div', class_="catalog__price")
                                   .text))
            price = ''.join(e for e in price if e.isalnum())
            city = "Москва"
            img_url = car.find("a").find('img').get("data-src")
            info.append(
                [brand, model, year, price, city, motor, transmission, wd, km,
                 href, img_url])
        except:
            print("WARNING: information could not be obtained from this link: "
                  "\"{}\"".format(url))
    # print(info)
    return info
