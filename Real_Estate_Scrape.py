import httpx
from bs4 import BeautifulSoup
import csv

URL = "https://hk.centanet.com/findproperty/en/list/buy"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Translation table

translation_dict = {"・": " "}
translation_table = str.maketrans(translation_dict)



with httpx.Client(verify=False) as client: 
    response = client.get(URL, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

results = soup.find_all("div", class_="main-content")

property_title_list = []
property_price_list = []
property_saleableArea_list = []
property_district_list = []

for element in results:
    
    property_titles = element.find_all("span", class_="title-lg")
    property_price = element.find_all("span", class_="price-info")
    property_saleableArea = element.find_all("span", class_="hidden-xs-only") #some issue here
    property_district = element.find_all("span", class_="adress tag-adress")

    #check no. of element
    print("Number of Titles:", len(property_titles))
    print("Number of Prices:", len(property_price))
    print("Number of Saleable Areas:", len(property_saleableArea))
    print("Number of district:", len(property_district))


    combined_list = zip(property_titles, property_price, property_saleableArea, property_district)
    #print(tuple(combined_list))

    for title, price, saList, districts in combined_list:
        raw_title_text = title.get_text(strip=True)
        cleaned_title_text = raw_title_text.translate(translation_table)
        #print(cleaned_title_text, end="\n")
        property_title_list.append(cleaned_title_text)

        price_text = price.get_text(strip=True)
        property_price_list.append(price_text)

        saList_text = saList.get_text(strip=True)
        property_saleableArea_list.append(saList_text)

        district_text = districts.get_text(strip=True)
        property_district_list.append(district_text)


with open("Property_name.csv", "w", encoding="utf-8", newline="") as property_name_csv:
    csv_writer = csv.writer(property_name_csv, delimiter=",")
    csv_header = ["Property", "Price", "S.A.", "District"]
    csv_writer.writerow(csv_header)

    for title, price, saleableArea, districts in zip(property_title_list, property_price_list, property_saleableArea_list, property_district_list):
        csv_writer.writerow([title, price, saleableArea, districts])

