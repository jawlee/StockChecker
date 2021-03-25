from selenium import webdriver
from bs4 import BeautifulSoup

from chromedriver_py import binary_path

import requests

from discord import Webhook, RequestsWebhookAdapter

discordwebhook = Webhook.from_url("https://discord.com/api/webhooks/824516450730901515/fCwDFCAQhqFgsErMgEh9rt8LKF-KzrgX-BIABDCHMfDv2YiDW2Aq3RUEe4hTFo7icGWC", adapter=RequestsWebhookAdapter())

driver = webdriver.Chrome(executable_path=binary_path)
urlList = [
    "https://www.amazon.ca/Dogs-Sofa-Jigsaw-Puzzle-Piece/dp/B07S9MP986/ref=pd_rhf_ee_s_rpt_age_toy_picks_0_2/139-8353022-5665244?_encoding=UTF8&pd_rd_i=B07S9MP986&pd_rd_r=a4963629-0d4b-46d2-ba8e-669d66612ef6&pd_rd_w=I2zVK&pd_rd_wg=LRnYP&pf_rd_p=824d06ea-8ce2-4797-8150-02f913554268&pf_rd_r=KGGR8NNPV2PAFPBQS81D&psc=1&refRID=KGGR8NNPV2PAFPBQS81D",
    #"https://www.amazon.ca/MSI-GeForce-RTX-3070-Architecture/dp/B08KWPDXJZ/ref=sr_1_6?dchild=1&keywords=rtx+3070&qid=1616651057&sr=8-6"
    ]
print ("\n\n\n")

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
        discordwebhook.send('' +stockStatus+ '\n' +url)
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


