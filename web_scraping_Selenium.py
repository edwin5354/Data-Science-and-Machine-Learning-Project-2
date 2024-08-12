import httpx
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
#from selenium.webdriver.edge import Edge


def find_infoTitle(driver):
    try:
        infoTitle = driver.find_element(By.CSS_SELECTOR, 'h1.info-title').text.strip()
    except Exception:
        infoTitle = ''
    return infoTitle

def findAddress(driver):
    try:
        address = driver.find_element(By.CSS_SELECTOR, 'span.font-mbl-15').text.strip()
    except Exception:
        address = ''
    return address

def findDistricts(driver):
    districts = []
    try:
        district_elements = driver.find_elements(By.CSS_SELECTOR, 'span.adress.tag-adress')
        for element in district_elements:
            districts.append(element.text.strip())
    except Exception:
        pass
    return districts

def findDevname(driver):
    try:
        dev_name = driver.find_element(By.CSS_SELECTOR, 'div.developerName').text.strip()
    except Exception:
        dev_name = ''
    return dev_name

def findPrice(driver):
    try:
        price = driver.find_element(By.CSS_SELECTOR, 'div.price-number').text.strip()
    except Exception:
        price = ''
    return price

def findArea(driver):
    try:
        area = driver.find_element(By.CSS_SELECTOR, 'span.area').text.strip()
    except Exception:
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

    # Set up the Edge driver
    path = r'C:\Xccelerate\Edge_Driver\msedgedriver.exe'
    service = Service(executable_path=path)
    driver = webdriver.Edge(service=service)

    # Create a dictionary that transforms into csv/ excel file
    d = {'title': [], 'address': [], 'district': [], 'devname': [], 
        'price': [], 'area': []}#, 'room': [], 'age':[]}

    #d = {'district': []}

    # url = 'https://hk.centanet.com/findproperty/en/list/buy'
    # webpage = requests.get(url, HEADERS)
    driver.get(url)
    time.sleep(0.5)



    total_no_page = 3
    for i in range(1, total_no_page + 1):

        # District in the main webpage
        districts = findDistricts(driver)
        d['district'].extend(districts)

        # Open new link to extract the data in a new webpage
        links = driver.find_elements(By.CSS_SELECTOR, 'a.property-text')
        #print(links)


        link_list = [link.get_attribute('href') for link in links]

        j = 1 # property-page counter

        for link in link_list:
            
            #driver.get(link)
            driver.execute_script(f"window.open('{link}', '_blank');") # JS code, open new tab
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1]) # JS code, switch tab

            j += 1 # property-page counter + 1

            d['title'].append(find_infoTitle(driver))
            d['address'].append(findAddress(driver))
            d['devname'].append(findDevname(driver))
            d['price'].append(findPrice(driver))
            d['area'].append(findArea(driver))
            #d['room'].append(roomCount(new_soup))
            #d['age'].append(roomAge(new_soup))
            
            print("Main sub-page: {}, property-page count: {}".format(i,j))
            driver.close() # close tab
            driver.switch_to.window(driver.window_handles[0]) # Switch Tab back to main page

        # driver.back() # ideal choice, return to previous page, may have to repeat 24 times
        j=1 # reset property-page counter
        driver.get(url) # return to main page, but sub-page selection return to sub-page 1
        time.sleep(0.5) 

        # Next Main sub-page
        if i < total_no_page:
            next_page_button = driver.find_element(By.XPATH, "//button[@class='btn-next']")
            driver.execute_script("arguments[0].scrollIntoView();", next_page_button)  # Scroll to the next-button
            time.sleep(0.5)
            next_page_button.click()
            time.sleep(0.5)
            


estate_df = pd.DataFrame.from_dict(d)
estate_df.to_csv("./csv/download.csv") # Store it somewhere in the local computer and publish it in Github
driver.quit()