import httpx
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time



user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
url = 'https://hk.centanet.com/findproperty/en/list/buy'
HEADERS = {'User-Agent': user_agent, 'Accept-Language': 'en-US, en;q=0.5'}

# Set up the Edge driver
path = r'C:\Xccelerate\Edge_Driver\msedgedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Edge(service=service)

driver.get(url)
next_page_button = driver.find_element(By.XPATH, "//button[@class='btn-next']")
#driver.execute_script("arguments[0].scrollIntoView();", next_page_button)  # Scroll to the next-button
time.sleep(0.5)
next_page_button.click()