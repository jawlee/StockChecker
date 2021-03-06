from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options

import concurrent.futures

import time
from datetime import datetime
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

from random import randrange

import configparser

from discord import Webhook, RequestsWebhookAdapter



cartUrl = "https://www.amazon.ca/gp/cart/view.html?ref_=nav_cart"

configFile = "AMZconfig.ini"



# Setup variables and User Info
def setup():
    config = configparser.ConfigParser()
    config.read(configFile)
    global loginID
    loginID = config['Amazon Info']['Username']
    global pwd
    pwd = config['Amazon Info']['password']
    
    # global foundStock 
    # foundStock = False

    dURL = config['Discord URL']['wURL']
    derrURL = config['Discord URL']['errURL']
    print(f"username = {loginID}")
    print(f"passowrd = {pwd}")
    print(f"discord URL = {dURL}")

    global discordwebhook
    discordwebhook = Webhook.from_url(dURL, adapter=RequestsWebhookAdapter())

    global errDiscord
    errDiscord = Webhook.from_url(derrURL, adapter=RequestsWebhookAdapter())

    global urlList 
    urlList = []   
    urlList_pre = config['URL List']['uList']
    urlList_pre.strip(',')
    urlList = urlList_pre.strip().splitlines()

    global ATCList 
    ATCList = []
    
    global boughtList
    boughtList = []

# Login function
def login():
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1080")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    # experimentalFlags = ['new-usb-backend@1']
    # chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
    # option.add_experimental_option('localState',chromeLocalStatePrefs)
    
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium") 
    option.add_argument("--enable-javascript")
    # option.add_argument('proxy-server=106.122.8.54:3128')

    global logindriver
    logindriver = webdriver.Chrome(executable_path=binary_path,options=option)
    logindriver.get("https://www.amazon.ca")
    time.sleep(1.5)
    content = logindriver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    logindriver.find_element_by_id('nav-link-accountList-nav-line-1').click()
    time.sleep(2)
    userForm = logindriver.find_element_by_class_name('auth-required-field').send_keys(loginID)    
    time.sleep(2)
    logindriver.find_element_by_id('continue').click()
    time.sleep(2)
    logindriver.find_element_by_id('ap_password').send_keys(pwd)
    logindriver.find_element_by_id('signInSubmit').click()
    time.sleep(2)

# Random number generator
def randomGen():
    pass
    # placeholder to random gen browser options
    # placeholder to random gen sleep time

# Add to cart function
def ATC(url):
    print("in ATC")
    print(f'ATCList length is: {len(ATCList)}')
    if len(ATCList) == 0:
        try:
            ATCList.append(url)
            logindriver.get(url)
            print('Login Session trying to add to cart')
            #error here
            logindriver.find_element_by_id("add-to-cart-button").click()
            print("Add to cart clicked")
            print(f'ATCList length is now: {len(ATCList)}')
            if url not in boughtList:
                BYN(url)
        except:
            ATCList.pop(0)
            print("Login Session Error. Unable to add to cart.")
            errDiscord('ERROR DETECTED')            
    else:
        print("Item in cart already.")
    print("quitting ATC")

def errDiscord(msg):
    errDiscord.send(msg)

def BYN(url):
    print("In BYN")
    # logindriver.get(url)
    print("BYN got URL")
    logindriver.get("https://www.amazon.ca/gp/buy/spc/handlers/display.html?hasWorkingJavascript=1")
    
    time.sleep(2)
    # logindriver.find_element_by_id('buy-now-button').click()
    # print('clicked Buy Now button')
    # time.sleep(3)
    # logindriver.find_element_by_id('turbo-checkout-pyo-button').click()
    # print('Clicked Place Your Order')

    deliv = logindriver.find_element_by_xpath('//input[@title="FREE Prime Delivery"]')
    print(deliv)
    deliv.click()
    logindriver.find_element_by_xpath('//input[@name="placeYourOrder1"]').click()
    print("Place Your Order button clicked")
    errDiscord('BOUGHT ONE!!!!!!!!')
    boughtList.append(url)
    print(f'boughtList count now: {len(boughtList)}')

# Check Stock function
def checkStock(url):
    
    time.sleep(1)
    startTime = time.perf_counter()
    #Open Browser
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1080")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    # experimentalFlags = ['new-usb-backend@1']
    # chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
    # option.add_experimental_option('localState',chromeLocalStatePrefs)
    # option.add_argument('proxy-server=106.122.8.54:3128')
    driver = webdriver.Chrome(executable_path=binary_path,options=option)
    print(f'{datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")} Checking Stock')
    
    driver.get(url)
    
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    # Parse Amazon website tags
    availMsg = soup.find('input', attrs={'id':'add-to-cart-button'})
    merchantInfo = soup.find('div', attrs={'id':'merchant-info'})  
    prcSoup = soup.find('span', attrs={'id':'priceblock_ourprice'})
    prodTitleSoup = soup.find('span', attrs={'id':'productTitle'})
   
    # Get product title
    productTitle = prodTitleSoup.text
    productTitle = ' '.join(productTitle.split())
    
    stockStatus ="Not defined yet"
    if availMsg is not None and "by Amazon" in merchantInfo.text:
        try:
            print("Found Add to Cart Button & Fulfilled by Amazon")
            ATC(url)         
            stockStatus='IN STOCK!!!!!!!!!!!!!'
            
            # Get product price
            productPrice = prcSoup.text
            productPrice = ' '.join(productPrice.split())
    
            discordwebhook.send(f'AMAZON STOCK ALERT!!!! {url}\nPrice: {productPrice}\nProduct: {productTitle}')
            print("Sent Discord message")
            
            #Save HTML to file
            # date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            # availFile_Amazon = open(f'Available_AMZ_{date}.txt',"w+")
            # availFile_Amazon.write(url+"\n\n")
            # availFile_Amazon.write(str(soup))
            # availFile_Amazon.close()
            # driver.find_element_by_id("add-to-cart-button").click()
        except:
            print("Issue Adding to Cart")
            errDiscord("Issue - Anonymous Add to Cart")
            pass
    else:
        stockStatus ="Not Available / Not Fulfilled by Amazon"
    print(f'Product: {productTitle}\nAvailability: {stockStatus}')
    endTime = time.perf_counter()
    totDurCheck = endTime - startTime
    print(f"Duration of script: {totDurCheck} seconds")
    print("===========================================================================\n")

def main():
    
    setup()
    login()
    
    print(urlList)
    print(f'Length of URL List is: {len(urlList)}')

    global MAX_THREADS
    MAX_THREADS = 2
    
    threads = min(MAX_THREADS, len(urlList))

    while(True):
        startTime = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(checkStock, u) for u in urlList]
        endTime = time.perf_counter()
        totDurCheck = endTime - startTime
        print(f"Finished Checking urlList in {totDurCheck} seconds")
        print(f'boughtList count now: {len(boughtList)}')
        print(f'ATCList length is: {len(ATCList)}')
        print(f'{datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")} Sleeping for 20 seconds')
        time.sleep(20)   
    
    # The below does not use multithreading
    # for u in urlList:
    #     checkStock(u)

    
if __name__ == "__main__":
    main()

