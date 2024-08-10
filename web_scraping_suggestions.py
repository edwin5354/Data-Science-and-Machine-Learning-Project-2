import httpx # Assuming you can extract the info using httpx; no idea why the hell i cannot even install it
from bs4 import BeautifulSoup
import requests
import pandas as pd

def find_infoTitle(soup):
    try:
        infoTitle = soup.find('h1', attrs = {'class': 'info-title'}).get_text(strip=True)
    except AttributeError:
        infoTitle = ''
    return infoTitle

def findAddress(soup):
    try:
        address = soup.find('span', attrs = {'class': 'font-mbl-15'}).get_text(strip=True)
    except AttributeError:
        address = ''
    return address

def findDistricts(soup):
    districts = []
    try:
        district_elements = soup.find_all('span', attrs={'class': 'adress tag-adress'})  
        for element in district_elements:
            districts.append(element.get_text(strip=True))
    except AttributeError:
        pass
    return districts

def findDevname(soup):
    try:
        dev_name = soup.find('div', attrs = {'class': 'developerName'}).get_text(strip=True)
    except AttributeError:
        dev_name = ''
    return dev_name

def findPrice(soup):
    try:
        price = soup.find('div', attrs = {'class': 'price-number'}).get_text(strip=True)
    except AttributeError:
        price = ''
    return price

def findArea(soup):
    try:
        area = soup.find('span', attrs = {'class': 'area'}).get_text(strip=True)
    except AttributeError:
        area = ''
    return area


# def grossArea(soup):
#     try:
#         area = soup.find('span', attrs = {'class': 'area'}).get_text(strip=True)
#     except AttributeError:
#         area = ''
#     return area


# def roomCount(soup):
#     try:
#         room_paragraph = soup.find('p', attrs={'class': 'info-tag'}, text=lambda t: 'Room' in t)
#         numRoom = room_paragraph.get_text(strip=True) if room_paragraph else ""
#     except AttributeError:
#         numRoom = ''
#     return numRoom

# def roomAge(soup):
#     try:
#         age_paragraph = soup.find('p', attrs={'class': 'info-tag'}, text=lambda t: 'Age' in t)
#         age = age_paragraph.get_text(strip=True) if age_paragraph else ""
#     except AttributeError:
#         age = ''
#     return age


if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    url = 'https://hk.centanet.com/findproperty/en/list/buy'
    HEADERS = {'User-Agent': user_agent, 'Accept-Language': 'en-US, en;q=0.5'}

    with httpx.Client(verify=False) as client: 
        response = client.get(url, headers=HEADERS)

    # Create a dictionary that transforms into csv/ excel file
    d = {'title': [], 'address': [], 'district': [], 'devname': [], 
        'price': [], 'area': []}#, 'room': [], 'age':[]}

    #d = {'district': []}

    # url = 'https://hk.centanet.com/findproperty/en/list/buy'
    # webpage = requests.get(url, HEADERS)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # District in the main webpage
    districts = findDistricts(soup)
    d['district'].extend(districts)

    # Open new link to extract the data in a new webpage
    links = soup.find_all('a', attrs={'class': 'property-text'})
    
    link_list = []


    # Extract unique links for different properties
    for link in links:
        link_list.append(link.get('href'))
    print('https://hk.centanet.com' + link_list[0])

    for link in link_list:
        with httpx.Client(verify=False) as client:
            new_webpage = client.get('https://hk.centanet.com' + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

            d['title'].append(find_infoTitle(new_soup))
            d['address'].append(findAddress(new_soup))
            d['devname'].append(findDevname(new_soup))
            d['price'].append(findPrice(new_soup))
            d['area'].append(findArea(new_soup))
            #d['room'].append(roomCount(new_soup))
            #d['age'].append(roomAge(new_soup))

estate_df = pd.DataFrame.from_dict(d)
estate_df.to_csv("./download.csv") # Store it somewhere in the local computer and publish it in Github
