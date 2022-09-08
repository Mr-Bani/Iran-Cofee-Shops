from bs4 import BeautifulSoup
from requests import get
from lxml import etree

def scrape_card(link):
    html = get(link).text
    soup = BeautifulSoup(html, "html.parser")

    #info list
    name = soup.find(property="name").text.strip()
    cafe_address = soup.find(property="address").text.strip()
    phone_number = soup.find(property="telephone").text.strip()

    #stars
    dom = etree.HTML(str(soup))
    working_hours = (dom.xpath('/html/body/div[2]/div/section[1]/section/div[4]/div[2]/section[2]/div[1]/div[2]/ul/li[3]/span/span')[0].text.strip())
    working_hours = working_hours.replace('ساعت کار کافه', '').strip()
    work_start, work_end = working_hours.split('-')
    food_quality = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[1]/span[2]/div")
    food_quality = (int(food_quality[0].attrib['data-rateit-value'].strip()))
    service_quality = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[2]/span[2]/div")
    service_quality = (int(service_quality[0].attrib['data-rateit-value'].strip()))
    cost_value = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[3]/span[2]/div")
    cost_value = (int(cost_value[0].attrib['data-rateit-value'].strip()))
    environment = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[4]/span[2]/div")
    environment = (int(environment[0].attrib['data-rateit-value'].strip()))

    #cost
    cost = dom.xpath("//*[@id=\"information\"]/hgroup/div[1]/div[1]/div/span[3]")[0]
    cost = int(cost.text.strip())

    features = dom.xpath("/html/body/div[2]/div/section[1]/section/div[4]/div[2]/section[1]/div[1]/div[2]/div[1]/div[2]/div[2]/span")
    features = [feature.text.strip() for feature in features]




scrape_card("https://fidilio.com/coffeeshops/melo/%D9%85%D9%84%D9%88/")