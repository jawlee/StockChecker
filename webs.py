from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from chromedriver_py import binary_path
import pickle

# import requests
import concurrent.futures

import time
from datetime import datetime
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

from random import randrange

import configparser

# import smtplib, ssl
# from email.message import EmailMessage
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login('', '')

# msg = EmailMessage()

# msg['Subject'] = " "
# msg['From'] = "1"
# msg['To'] = ['xxxxxxxxx@pcs.rogers.com']

import requests

from discord import Webhook, RequestsWebhookAdapter
# Set up
# Chrome / Discord
# List of URLs
discordwebhook = ''
urlList = [
        "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285",
        "https://www.bestbuy.ca/en-ca/product/evga-nvidia-geforce-rtx-3060-ti-ftw3-ultra-8gb-gddr6-video-card/15229237",
        "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3070-8gb-gddr6-video-card-only-at-best-buy/15078017",
        "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3070-xc3-ultra-8gb-gddr6-video-card/15147122",
        "https://www.bestbuy.ca/en-ca/product/msi-nvidia-geforce-rtx-3070-ventus-3x-oc-8gb-gddr6-video-card/15038016",
        "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6x-video-card/15084753",
        "https://www.bestbuy.ca/en-ca/product/asus-tuf-gaming-nvidia-geforce-rtx-3080-10gb-gddr6x-video-card/14953248",
        # "https://www.bestbuy.ca/en-ca/product/bioshock-the-collection-switch/14538667"
        ]

global MAX_THREADS
MAX_THREADS = 3

configFile = "BBconfig.ini"

# Setup variables and User Info
def setup():
    config = configparser.ConfigParser()
    config.read(configFile)

    global loginID
    loginID = config['BB Info']['Username']
    global pwd
    pwd = config['BB Info']['password']
    
    dURL = config['Discord URL']['wURL']
    print(f"username = {loginID}")
    print(f"passowrd = {pwd}")
    print(f"discord URL = {dURL}")

    discordwebhook = Webhook.from_url(dURL, adapter=RequestsWebhookAdapter())  

def login():
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1080")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium") 
    # option.add_argument('proxy-server=106.122.8.54:3128')

    global logindriver
    logindriver = webdriver.Chrome(executable_path=binary_path,options=option)
    logindriver.get("https://www.bestbuy.ca")
    time.sleep(3)
    content = logindriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    logindriver.find_element_by_class_name('signInOutNavContainer_2mwkw').click()
    time.sleep(3)
    logindriver.find_element_by_id('username').send_keys(loginID)
    time.sleep(3)
    logindriver.find_element_by_id('password').send_keys(pwd)
    time.sleep(3)
    logindriver.find_element_by_class_name('GSYpm').click()
    time.sleep(3)
    print(loginID)
    print(pwd)


# Random number generator
# TODO
def randNum(num):
    return randrange(num)
    # placeholder to random gen browser options
    # placeholder to random gen sleep time

def saveHTML(page):
#Save HTML to file
    availFile = open(f"Available_BB_{date}.txt","w+")
    availFile.write(page)
    availFile.close()

# Add to cart function
def ATC(url):
    try:
        logindriver.get(url)
        logindriver.find_element_by_class_name("addToCartButton_1op0t").click()
        print("Add to cart clicked")
        time.sleep(1.5)   
        logindriver.get("https://www.bestbuy.ca/en-ca/basket")
    except:
        print("Could not click on button.")

# Stock check function
def checkStock(url):
    #Open Browser
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1080")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    # option.add_argument('proxy-server=106.122.8.54:3128')
    driver = webdriver.Chrome(executable_path=binary_path,options=option)
    
    # Remove navigator.webdriver Flag using JavaScript
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  

    # Start checking for stock

    driver.get(url)
    
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    availMSg=soup.find('span', attrs={'class':'availabilityMessage_ig-s5 container_3LC03'})
    print("Checking stock status")
    # Check stock status
    if "Coming soon" in availMSg:
        stockStatus='COMING SOON'
    elif "Available to ship" in availMSg:
        ATC(url)

         # message = f'IN STOCK!!! \n{url}\n'
        # msg.set_content(message)
        # try:
        #     server.send_message(msg)
        #     print("email sent!!")
        # except:
        #     print("Email not sent! Something wrong")

        # saveHTML(soup)
        discordwebhook.send('@gpu-stock BB STOCK ALERT!\n' +url)
        stockStatus='IN STOCK!!!!!!!!!!!!!'
        
    else:
        print('Neither Coming Soon or Available to ship')
    time.sleep(5)
    driver.close()
    print(url)
    print(''+date+': Availability is: ' +stockStatus)
    # print(availMSg)
    print ("===========================================================================\n")

def main():
    startTime = time.perf_counter()
    setup()
    login()

    time.sleep(10)
    
    threads = min(MAX_THREADS, len(urlList))
    while (True):
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(checkStock, urlList)
        print("Rechecking in 30 seconds")
        time.sleep(30)

    endTime = time.perf_counter()
    totDurCheck = endTime - startTime  
    
    print(f"Duration of script: {totDurCheck} seconds")

if __name__ == '__main__':
    main()