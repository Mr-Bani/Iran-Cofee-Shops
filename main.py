# -*- coding:utf-8 -*-
from scrape_card import *
from sql_connector import *
from fidilio_links import cafe_links
from page_number import cities_page_number



sql = sql_connector(user="user_group2", password="sBTdgyAxvrEs_group2", host="45.139.10.138",port=80, database="group2")

cities = cities_page_number("restaurants")


failed = []



for city,max_number in cities.items():
    for i in range(int(max_number)+1):
        for link in cafe_links("https://fidilio.com/restaurants/in/"+city+"/?p="+str(i)):
            try:
                sql.insert(scrape_card(link,city,2))
            except:
                failed.append(link)
