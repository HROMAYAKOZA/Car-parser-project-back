import unicodedata

from bs4 import BeautifulSoup
import requests
from requests import Response


def create_info(name, href, price, city, components: str) -> str:
    data = components.split(',')
    return "\n{0} ({2}):" \
           "\n\tЦена: {1}" \
           "\n\tГород: {3}" \
           "\n\tДвигатель: {4}, {5} " \
           "\n\tКоробкак передач: {6} " \
           "\n\tПривод: {7}".format(name, price, href, city, data[0], data[1], data[2], data[3])


def create_html(url: str) -> Response:
    html_code = requests.get(url)
    # print("-------------------------------------------------------\n"
    #       "Connection status : {}\n".format(html_code.status_code))
    return html_code


def get_info(url: str) -> list:
    soup = BeautifulSoup(create_html(url).text, "html.parser")
    allCars = soup.findAll('a', class_="css-xb5nz8 e1huvdhj1")
    info = []
    for car in allCars:
        try:
            name = car.find('div', class_="css-1wgtb37 e3f4v4l2").find('span').text
            specifications = car.find("div", class_="css-1fe6w6s e162wx9x0").find_all("span")
            components = ""

            for parameter in specifications:
                components += parameter.text + " "
            components = components.split(',')
            motor = "{},{}".format(components[0], components[1])
            transmission = components[2].strip()
            wd = components[3].strip()

            href = car.get("href").strip()
            price = unicodedata.normalize("NFKD", "{}₽".format(car
                                                               .find('span', class_="css-46itwz e162wx9x0")
                                                               .find('span')
                                                               .text))
            city = car.find('div', class_="css-1x4jcds eotelyr0").find('span').text

            info.append([name, href, price, city, motor, transmission, wd])
        except:
            pass
    return info


def get_full_info(url: str) -> list:
    page = 0
    full_info = []
    while page <= 2:
        url = url.replace(f"page{page}", f"page{page + 1}")
        # print(url)
        page += 1
        for p in get_info(url):
            # print(p)
            full_info.append(p)
    # print(full_info)
    return full_info


def edit_url(info: dict[str, str]) -> str:
    if info.get("price_from") != "" and info.get("price_to") != "":
        return "https://{}.drom.ru/{}/{}/page1/?minprice={}&maxprice={}".format(info.get("city"),
                                                                          info.get("brand"),
                                                                          info.get("model"),
                                                                          info.get("price_from"),
                                                                          info.get("price_to"))
    elif info.get("price_from") != "":
        return "https://{}.drom.ru/{}/{}/page1/?minprice={}".format(info.get("city"),
                                                              info.get("brand"),
                                                              info.get("model"),
                                                              info.get("price_from"))
    elif info.get("price_to") != "":
        return "https://{}.drom.ru/{}/{}/page1/?maxprice={}".format(info.get("city"),
                                                              info.get("brand"),
                                                              info.get("model"),
                                                              info.get("price_to"))
    return "https://{}.drom.ru/{}/{}/page1/".format(info.get("city"), info.get("brand"), info.get("model"))
