from selenium import webdriver
from bs4 import BeautifulSoup

from chromedriver_py import binary_path

import requests

from datetime import datetime

date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

from discord import Webhook, RequestsWebhookAdapter
# Set up Discord
discordwebhook = Webhook.from_url("https://discord.com/api/webhooks/824516450730901515/fCwDFCAQhqFgsErMgEh9rt8LKF-KzrgX-BIABDCHMfDv2YiDW2Aq3RUEe4hTFo7icGWC", adapter=RequestsWebhookAdapter())

#Set up Chrome
driver = webdriver.Chrome(executable_path=binary_path)

urlList = [
    "https://www.amazon.ca/Dogs-Sofa-Jigsaw-Puzzle-Piece/dp/B07S9MP986/",
    "https://www.amazon.ca/MSI-GeForce-RTX-3070-Architecture/dp/B08KWPDXJZ/",
    "https://www.amazon.ca/EVGA-GeForce-3060-Graphics-08G-P5-3663-KR/dp/B08R876RTH/",
    "https://www.amazon.ca/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ",
    "https://www.amazon.ca/Graphics-IceStorm-Advanced-Lighting-ZT-A30700H-10P/dp/B08LF1CWT2",
    "https://www.amazon.ca/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ/"
    ]
print ("Done Setup\n\n\n")

for url in urlList:
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    availMsg=soup.find('span', attrs={'class':'a-color-success'})
    print("availMsg is: ")
    print(availMsg)

    if "Coming soon" in availMsg:
        stockStatus='COMING SOON'
    elif "In Stock" in availMsg:
        driver.find_element_by_id("add-to-cart-button").click()
        stockStatus='IN STOCK!!!!!!!!!!!!!'
        discordwebhook.send('@gpu-stock AMAZON STOCK ALERT!\n' +url)

        #Save HTML to file
            availFile_Amazon = open("Available_AMZ_"+date+".txt","w+")
            availFile_Amazon.write(url+"\n\n")
            availFile_Amazon.write(soup)
            availFile_Amazon.close()
    else:
        stockStatus ="elsenothing"
        print('something else')
        driver.find_element_by_id("add-to-cart-button").click()
    print ("===========================================================================\n")
    print(url)
    print('Availability is: ' +stockStatus)
    print(availMsg)
    print ("===========================================================================\n")

# print ("html file")
#print(soup)


