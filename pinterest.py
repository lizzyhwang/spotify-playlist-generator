# code based on https://github.com/robertomape/PinterestImageScraper/blob/main/pinterestscraper.py
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import requests
import os

# returns the url to a pinterest image
def getImageUrl(searchTerm: str):
    url = f'https://in.pinterest.com/search/pins/?q=' + \
        searchTerm.replace(" ", '%20')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    driver.get(url)
    driver.implicitly_wait(15)

    all_pin_data = []

    while 1:
        time.sleep(3)

        # get the html 
        page_source = driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')

        # Here we take divs which have a with href as pin number
        images = page.find_all('div', "Yl- MIw Hb7")

        all_pin_data.extend(images)
        all_pin_data = list(set(all_pin_data))
        if len(all_pin_data) > 5:
            break

    hrefs = []
    for i in range(len(all_pin_data)):
        hrefs.append(all_pin_data[i].find('img')['src'])

    idx = random.randint(0,len(hrefs)-1)
    if hrefs[idx].find("/236x/") != -1:
        return hrefs[idx].replace("/236x/","/736x/")
    return hrefs[idx]

def getPlaylistCoverImage(searchTerm: str):
    img_url = getImageUrl(searchTerm + " aesthetic")
    img_data = requests.get(img_url).content

    # Save the image
    if not os.path.exists("images/"):
        os.makedirs("images/")
    filename = searchTerm.replace(" ", "_")
    filename += '_playlist_cover'
    with open(f'images/{filename}.jpeg', 'wb') as data_handler:
        data_handler.write(img_data)