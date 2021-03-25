from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import pandas as pd

import chromedriver_install as cdi

path = cdi.install(file_directory='c:\\data\\chromedriver\\', verbose=True, chmod=True, overwrite=False, version=None)
print('Installed chromedriver to path: %s' % path)

driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe")
driver.get("https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3070-xc3-ultra-8gb-gddr6-video-card/15147122")

content = driver.page_source
soup = BeautifulSoup(content)
# for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
availMSg=soup.find('span', attrs={'class':'availabilityMessage_ig-s5 container_3LC03'})
if availMSg = "Coming soon":
    print('availability is: ' +availMSg)
    print('\n\n')
else
    print('Not Coming soon')

print ("=========================")
print ("html file")
print(soup)

driver.find_element_by_class_name("button_2m0Gt primary_RXOwf addToCartButton_1op0t addToCartButton regular_23pTm").click()