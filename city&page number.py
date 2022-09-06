#find links (city name + page number)

import requests
from bs4 import BeautifulSoup

#find option tags for cities
url = 'https://fidilio.com/coffeeshops/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
urls = []
for link in soup.find_all('option'):
    print(link.get('value'))

#find the maximum number of pages
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get("https://fidilio.com/coffeeshops", headers = headers)
soup = BeautifulSoup(response.text,'lxml')
pages = soup.select('div.pagination a')
print(pages[-1].text)


