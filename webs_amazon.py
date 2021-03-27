from selenium import webdriver
from bs4 import BeautifulSoup

from chromedriver_py import binary_path

# import requests
import concurrent.futures

from datetime import datetime
import time

from discord import Webhook, RequestsWebhookAdapter

urlList = [
    "https://www.amazon.ca/Dogs-Sofa-Jigsaw-Puzzle-Piece/dp/B07S9MP986/",
    # "https://www.amazon.ca/MSI-GeForce-RTX-3070-Architecture/dp/B08KWPDXJZ/",
    # "https://www.amazon.ca/EVGA-GeForce-3060-Graphics-08G-P5-3663-KR/dp/B08R876RTH/",
    "https://www.amazon.ca/MSI-MAG-Core-Liquid-360R/dp/B087YL4DDY",
    "https://www.amazon.ca/Asus-RT-AC68U-Wireless-Dual-Band-Gigabit/dp/B00FB45SI4",
    # "https://www.amazon.ca/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ",
    # "https://www.amazon.ca/Graphics-IceStorm-Advanced-Lighting-ZT-A30700H-10P/dp/B08LF1CWT2",
    # "https://www.amazon.ca/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ/"
    ]

cartUrl = "https://www.amazon.ca/gp/cart/view.html?ref_=nav_cart"

MAX_THREADS = 30


# Function to instantiate all global vars 
def setup():
    # Set up Discord
    discordwebhook = Webhook.from_url("https://discord.com/api/webhooks/825198944673464380/APoOZe7FHZ-mT5w5o7CAq6-R9zlmb79HwT7xeliWQi9JbErhrnYam_cnK9T9dc7wegge", adapter=RequestsWebhookAdapter())


# Check Stock function
def checkStock(url):
    setup()
    startCheckTime = time.perf_counter()
    driver = webdriver.Chrome(executable_path=binary_path)
    driver.get(url)
    endCheckTime = time.perf_counter()

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    availMsg = soup.find('input', attrs={'id':'add-to-cart-button'})
    merchantInfo = soup.find('div', attrs={'id':'merchant-info'})  
    prcSoup = soup.find('span', attrs={'id':'priceblock_ourprice'})
    prodTitleSoup = soup.find('span', attrs={'id':'productTitle'})
    
    # print("availMsg is: ")
    # print(availMsg)
    
    stockStatus ="Not defined yet"
    # print(f"merchantInfo is: {merchantInfo.text}")
    if availMsg is not None and "by Amazon" in merchantInfo.text:
        
        try:
            # driver.find_element_by_id("add-to-cart-button").click()
            # print("Added to Cart")
            stockStatus='IN STOCK!!!!!!!!!!!!!'
            
            productPrice = prcSoup.text
            productPrice = ' '.join(productPrice.split())

            productTitle = prodTitleSoup.text
            productTitle = ' '.join(productTitle.split())

            print(f"Product: {productTitle}")
            print(f"Price: {productPrice}")
            discordwebhook.send(f'AMAZON STOCK ALERT!'+url)
            discordwebhook.send(f'Price: {productPrice}\nProduct: {productTitle}')
            discordwebhook.send(f'Cart URL: {cartUrl}')
            # print("Sent Discord message")
            
            #Save HTML to file
            # date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            # availFile_Amazon = open(f'Available_AMZ_{date}.txt',"w+")
            # availFile_Amazon.write(url+"\n\n")
            # availFile_Amazon.write(str(soup))
            # availFile_Amazon.close()
            # driver.find_element_by_id("add-to-cart-button").click()
        except:
            print("Issue Adding to Cart")
            pass
    else:
        stockStatus ="Not Available / Not Fulfilled by Amazon"
        # print(stockStatus)
    
    print(url)
    print('Availability: ' +stockStatus)
    
    durCheck = endCheckTime - startCheckTime
    print(f"Duration of process: {durCheck} seconds")
    print("===========================================================================\n")

def main():
    startTime = time.perf_counter()
    
    threads = min(MAX_THREADS, len(urlList))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(checkStock, urlList)
    
    # The below does not use multithreading
    # for u in urlList:
    #     checkStock(u)

    endTime = time.perf_counter()
    totDurCheck = endTime - startTime
    print(f"Duration of script: {totDurCheck} seconds")
    

if __name__ == "__main__":
    main()

