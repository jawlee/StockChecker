from selenium import webdriver
from bs4 import BeautifulSoup

from chromedriver_py import binary_path

import requests

from datetime import datetime


import time

from discord import Webhook, RequestsWebhookAdapter

urlList = [
    "https://www.amazon.ca/Dogs-Sofa-Jigsaw-Puzzle-Piece/dp/B07S9MP986/",
    "https://www.amazon.ca/MSI-GeForce-RTX-3070-Architecture/dp/B08KWPDXJZ/",
    "https://www.amazon.ca/EVGA-GeForce-3060-Graphics-08G-P5-3663-KR/dp/B08R876RTH/",
    # "https://www.amazon.ca/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ",
    # "https://www.amazon.ca/Graphics-IceStorm-Advanced-Lighting-ZT-A30700H-10P/dp/B08LF1CWT2",
    # "https://www.amazon.ca/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ/"
    ]

def setup():
    startSetupTime = time.perf_counter()

    # Set up Date
    global date 
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    
    # Set up Discord
    global discordwebhook 
    discordwebhook = Webhook.from_url("https://discord.com/api/webhooks/824516450730901515/fCwDFCAQhqFgsErMgEh9rt8LKF-KzrgX-BIABDCHMfDv2YiDW2Aq3RUEe4hTFo7icGWC", adapter=RequestsWebhookAdapter())

    #Set up Chrome
    global driver 
    driver = webdriver.Chrome(executable_path=binary_path)

    
    endSetupTime = time.perf_counter()
    dur = endSetupTime - startSetupTime
    print (f"Done Setup in {dur} seconds\n\n\n")

def checkStock(url):
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    availMsg = soup.find('input', attrs={'id':'add-to-cart-button'})
    merchantInfo = soup.find('a', attrs={'id':'SSOFpopoverLink'})
    # print("availMsg is: ")
    # print(availMsg)

    stockStatus ="Not defined yet"

    if availMsg is not None and "Fulfilled by Amazon" in merchantInfo:
        try:
            driver.find_element_by_id("add-to-cart-button").click()

            stockStatus='IN STOCK!!!!!!!!!!!!!'
            # discordwebhook.send('@gpu-stock TESTING!!!! AMAZON STOCK ALERT!\n' +url)

            #Save HTML to file
            # availFile_Amazon = open(f'Available_AMZ_{date}.txt',"w+")
            # availFile_Amazon.write(url+"\n\n")
            # availFile_Amazon.write(str(soup))
            # availFile_Amazon.close()
            # driver.find_element_by_id("add-to-cart-button").click()
        except:
            pass
    else:
        stockStatus ="Not Available / Not Fulfilled by Amazon"
        # print(stockStatus)
        
    print("===========================================================================\n")
    print(url)
    print('Availability is: ' +stockStatus)

def main():
    setup()
    print(urlList)
    for u in urlList:
        startCheckTime = time.perf_counter()
        checkStock(u)
        endCheckTime = time.perf_counter()
        durCheck = endCheckTime - startCheckTime
        print(f"Duration: {durCheck} seconds")

if __name__ == "__main__":
    main()

