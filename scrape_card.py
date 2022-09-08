from bs4 import BeautifulSoup
from requests import get
from lxml import etree
import datetime

all_features=[("دستگاه کارت خوان","pos"),("ارسال رایگان (Delivery)","delivery"),("اینترنت رایگان","internet"),("موسیقی زنده","live_music"),("سیگار","smoking"),("فضای باز","open_space"),("پارکینگ","parking"),("قلیان","hookah")]


def scrape_card(link,city):
    data=dict()

    html = get(link).text
    soup = BeautifulSoup(html, "html.parser")


    #info list
    cafe_name = soup.find(property="name").text.strip()
    cafe_address = soup.find(property="address").text.strip()
    phone_number = soup.find(property="telephone").text.strip()

    data["cafe_name"] = cafe_name
    data["cafe_address"] = cafe_address
    data["phone_number"] = phone_number
    data["city"] = city
    data["province"] =  data['cafe_address'].split('،')[0]



    #stars
    dom = etree.HTML(str(soup))
    working_hours = (dom.xpath('/html/body/div[2]/div/section[1]/section/div[4]/div[2]/section[2]/div[1]/div[2]/ul/li[3]/span/span')[0].text.strip())
    working_hours = working_hours.replace('ساعت کار کافه', '').strip()
    work_start, work_end = working_hours.split('-')
    if not work_start.__contains__(":"):
        work_start+=":00"
    work_start+=":00"

    if not work_end.__contains__(":"):
        work_end+=":00"
    work_end+=":00"

    food_quality = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[1]/span[2]/div")
    food_quality = (int(food_quality[0].attrib['data-rateit-value'].strip()))
    service_quality = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[2]/span[2]/div")
    service_quality = (int(service_quality[0].attrib['data-rateit-value'].strip()))
    cost_value = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[3]/span[2]/div")
    cost_value = (int(cost_value[0].attrib['data-rateit-value'].strip()))
    environment = dom.xpath("//*[@id=\"review-list\"]/div[1]/div[1]/ul/li[4]/span[2]/div")
    environment = (int(environment[0].attrib['data-rateit-value'].strip()))

    data["work_start"] = work_start
    data["work_end"] = work_end
    data["food_quality"] = food_quality
    data["service_quality"] = service_quality
    data["cost_value"] = cost_value
    data["environment"] = environment


    #cost
    price_class = soup.find("div", {"class": "price-class"})
    cost = int(price_class.find_all("span")[-1].text.strip())

    data["cost"] = cost

    features = dom.xpath("/html/body/div[2]/div/section[1]/section/div[4]/div[2]/section[1]/div[1]/div[2]/div[1]/div[2]/div[2]/span")
    features = [feature.text.strip() for feature in features]
    for persian_feature,feature in all_features:
        data[feature] = persian_feature in features

    return data

#print(scrape_card("https://fidilio.com/coffeeshops/dantecaferestaurant/%D8%AF%D8%A7%D9%86%D8%AA%D9%87/"))
