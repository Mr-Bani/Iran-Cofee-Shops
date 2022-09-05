import requests
from bs4 import BeautifulSoup


def cafe_names(page_url):
    url = page_url
    response = requests.get(url)
    html = response.text
    name_soup = BeautifulSoup(html, "html.parser")

    cafe_names = []
    for names in name_soup.find_all("div", {"class": "venue-title"}):
        cafe_names.append(names['title'])
    return cafe_names


def price_level(page_url):
    url = page_url
    response = requests.get(url)
    html = response.text
    price_soup = BeautifulSoup(html, "html.parser")

    names = cafe_names(url)

    pricelevels = price_soup.find_all("span", {"class": "price-class"})

    levels = dict()
    for n, item in enumerate(pricelevels):
        levels[names[n]] = len(item.find_all("span", {"class": "active"}))

    return levels


def cafe_links(page_url):
    url = page_url
    response = requests.get(url)
    html = response.text
    cart_soup = BeautifulSoup(html, "html.parser")

    main_url = 'https://fidilio.com/'

    cafe_links = []
    for links in cart_soup.find_all("a", {"class": "restaurant-link"}):
        cafe_links.append(main_url + links['href'])

    return cafe_links
