from selenium import webdriver
from bs4 import BeautifulSoup

from chromedriver_py import binary_path

import smtplib, ssl
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

discordwebhook = Webhook.from_url("https://discord.com/api/webhooks/824516450730901515/fCwDFCAQhqFgsErMgEh9rt8LKF-KzrgX-BIABDCHMfDv2YiDW2Aq3RUEe4hTFo7icGWC", adapter=RequestsWebhookAdapter())

driver = webdriver.Chrome(executable_path=binary_path)
urlList = [
    "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3070-xc3-ultra-8gb-gddr6-video-card/15147122",
    "https://www.bestbuy.ca/en-ca/product/bioshock-the-collection-switch/14538667"
    ]
print ("\n\n\n\n\n")

for url in urlList:
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    availMSg=soup.find('span', attrs={'class':'availabilityMessage_ig-s5 container_3LC03'})


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
        stockStatus='IN STOCK!!!!!!!!!!!!!'
        discordwebhook.send('' +stockStatus+ '\n' +url)
    else:
        print('something else')
    print ("===========================================================================\n")
    print(url)
    print('Availability is: ' +stockStatus)
    print(availMSg)
    print ("===========================================================================\n")

# print ("html file")
#print(soup)


