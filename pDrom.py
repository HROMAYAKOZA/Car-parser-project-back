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
    print("-------------------------------------------------------\n"
          "Connection status : {}\n".format(html_code.status_code))
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

            href = car.get("href").strip()
            price = "{}₽".format(car.find('span', class_="css-46itwz e162wx9x0").find('span').text)
            city = car.find('div', class_="css-1x4jcds eotelyr0").find('span').text
            info.append(create_info(name, href, price, city, components))

        except:
            pass
    return info


def get_full_info(url: str):
    page = 0
    while True:
        url = url.replace(f"page{page}", f"page{page + 1}")
        page += 1
        for p in get_info(url):
            print(p)


get_full_info("https://moscow.drom.ru/toyota/all/page1")
