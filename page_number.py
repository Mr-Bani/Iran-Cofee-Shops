#find links (city name + page number)

import requests
from bs4 import BeautifulSoup
from lxml import etree


#find option tags for cities
def cities(type):
    url = f'https://fidilio.com/{type}/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    cities=[]
    for link in soup.find_all('option'):
        if(link.get('value')=='0'):
            break
        cities.append(link.get('value'))

    return cities


def cities_page_number(type):
    cities_=cities(type)
    res=dict()
    for city in cities_:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(f"https://fidilio.com/{type}/in/"+city, headers = headers)
        soup = BeautifulSoup(response.text,'html.parser')
        dom = etree.HTML(str(soup))
        pages = dom.xpath('/html/body/div[2]/div/section[1]/section/div[2]/div/div/div[1]/div[2]/div/a')[-1]
        max_number = ((pages.values())[0].split('?')[1].split('=')[1])
        res[city] = max_number
    return res



