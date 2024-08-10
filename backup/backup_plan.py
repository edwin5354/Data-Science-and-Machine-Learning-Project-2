import pandas as pd  
from bs4 import BeautifulSoup  
import requests

# Web scraping  
url = "https://www.vijaysales.com/mobiles-and-tablets/type/buy-iphones-mobile-phone"


webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')
product_names = soup.find_all('h2', class_='BcktPrdNm_')

name_list = []
for product in product_names:
    name_list.append(product.text.strip())  

print((name_list))

# Scrap the following website <Response [200]>
# Plug https://www.plug.tech/collections/apple-iphones
# Croma https://www.croma.com/phones-wearables/mobile-phones/iphones/c/97
# Gazelle https://buy.gazelle.com/collections/iphones
# vijaysales https://www.vijaysales.com/mobiles-and-tablets/type/buy-iphones-mobile-phone
