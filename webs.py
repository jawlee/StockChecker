from selenium import webdriver
from bs4 import BeautifulSoup

from chromedriver_py import binary_path
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")


import time

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
discordwebhook = Webhook.from_url("https://discord.com/api/webhooks/824516450730901515/fCwDFCAQhqFgsErMgEh9rt8LKF-KzrgX-BIABDCHMfDv2YiDW2Aq3RUEe4hTFo7icGWC", adapter=RequestsWebhookAdapter())

driver = webdriver.Chrome(executable_path=binary_path)
urlList = [
    "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285",
    "https://www.bestbuy.ca/en-ca/product/evga-nvidia-geforce-rtx-3060-ti-ftw3-ultra-8gb-gddr6-video-card/15229237",
    "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3070-8gb-gddr6-video-card-only-at-best-buy/15078017",
    "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3070-xc3-ultra-8gb-gddr6-video-card/15147122",
    "https://www.bestbuy.ca/en-ca/product/msi-nvidia-geforce-rtx-3070-ventus-3x-oc-8gb-gddr6-video-card/15038016",
    "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6x-video-card/15084753",
    "https://www.bestbuy.ca/en-ca/product/asus-tuf-gaming-nvidia-geforce-rtx-3080-10gb-gddr6x-video-card/14953248",
    "https://www.bestbuy.ca/en-ca/product/bioshock-the-collection-switch/14538667"
    ]
print ("Done Setup\n\n\n\n\n")

# Start checking for stock
for url in urlList:
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    availMSg=soup.find('span', attrs={'class':'availabilityMessage_ig-s5 container_3LC03'})

    # Check stock status
    if "Coming soon" in availMSg:
        stockStatus='COMING SOON'
    elif "Available to ship" in availMSg:
        # message = f'IN STOCK!!! \n{url}\n'
        # msg.set_content(message)
        # try:
        #     server.send_message(msg)
        #     print("email sent!!")
        # except:
        #     print("Email not sent! Something wrong")

        # driver.find_element_by_class_name("addToCartButton_1op0t").click()
        try:
            atcbutton = EC.element_to_be_clickable((By.CLASS_NAME, "addToCartButton_1op0t"))
            time.sleep(2)
            atcbutton.click()
            print("Add to cart clicked")
            
            #Save HTML to file
            availFile = open("Available_BB_"+date+".txt","w+")
            availFile.write(url+"\n\n")
            availFile.write(soup)
            availFile.close()
        except:
            print("Could not click on button.")
        stockStatus='IN STOCK!!!!!!!!!!!!!'
        discordwebhook.send('@gpu-stock BB STOCK ALERT!\n' +url)
    else:
        print('Neither Coming Soon or Available to ship')
    print ("===========================================================================\n")
    print(url)
    print(''+date+': Availability is: ' +stockStatus)
    print(availMSg)
    print ("===========================================================================\n")
