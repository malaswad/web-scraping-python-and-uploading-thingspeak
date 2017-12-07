import httplib2, urllib
import http.client
from time import localtime, strftime
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
from datetime import datetime
import requests

def thingspeak(price_bit,google_price,facebook_price,price_snapchat,amazon_price,apple_price,walmart_price):
    params = urllib.parse.urlencode({'field1': price_bit,'field2': google_price,'field3': facebook_price,'field4': price_snapchat,'field5': amazon_price, 'field6': apple_price, 'field7': walmart_price,'key': 'LTOWSNYXG7RAG4OG'})
    headers = {"Content-type":
                   "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        conn.close()
        print("Upload Successfully")
    except:
        print("connection failed")

def get_price(my_url,x):

    #print(my_url)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')
    if x==1:
        stocks = page_soup.find('span', attrs={'class': 'bld'})
    else:
        stocks = page_soup.find('span', attrs={'class': 'pr'})

    #print(stocks)

    price_bit_temp = stocks.text.strip('USD')
    price_bit = price_bit_temp.replace(',','')

    return price_bit

# sleep for 60 seconds (api limit of 15 secs)
while True:
    print('Stocks prices')

    bit_coin_url = 'https://finance.google.com/finance?q=CURRENCY%3ABTC&ei=A0gHWoiXL865eqqviIAF'
    google_url= 'https://finance.google.com/finance?ei=_XQTWviBHNCWmAGui6fACA&q=google'
    facebook_url = 'https://finance.google.com/finance?q=NASDAQ%3AFB&ei=NngTWun3LsKpmAHX9ougCA'
    snapchat_url = 'https://finance.google.com/finance?q=NYSE:SNAP'
    amazon_url = 'https://finance.google.com/finance?q=amazon'
    apple_url = 'https://finance.google.com/finance?q=apple'
    walmart_url = 'https://finance.google.com/finance?q=walmart'

    price_bit = get_price(bit_coin_url,1)
    print('Price of bitcoin: ' + str(float(price_bit)))

    price_google = get_price(google_url,2)
    print('Price of Google: ' + str(float(price_google)))

    price_facebook = get_price(facebook_url,3)
    print('Price of Facebook: ' + str(float(price_facebook)))

    price_snapchat = get_price(snapchat_url,4)
    print('Price of Snapchat: ' + str(float(price_snapchat)))

    amazon_price = get_price(amazon_url,5)
    print('Price of Amazon: ' + str(float(amazon_price)))

    apple_price = get_price(apple_url, 6)
    print('Price of Apple: ' + str(float(apple_price)))

    walmart_price = get_price(walmart_url, 7)
    print('Price of Walmart: ' + str(float(walmart_price)))

    #price_bit_float = float(price_bit)
    thingspeak(price_bit,price_google,price_facebook,price_snapchat,amazon_price,apple_price,walmart_price)

    prices = [price_bit, price_google, price_facebook, price_snapchat, amazon_price, apple_price, walmart_price]
    #print(prices)
    #prices_float = map(float, prices)
    prices_float = [float(i) for i in prices]
    prices_float_final = [format(datetime.now().date()), format(datetime.now().time())] + prices_float

    try:
        with open('stock_price.csv','a') as csv_file:
            csv.writer(csv_file).writerow(prices_float_final)
    except Exception as e:
        print("Couldn't write to the file due to "+ str(e))

    print("Twitting by thingtweet program")
    API_KEY = '0A6U41N3X1XO7EIO'
    url = "http://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key="
    fill = "&status="
    url = url + API_KEY + fill
    tweet = ('Bitcoin:''\n' +(price_bit)[0:7]+'\n'+'Google:'+(price_google)+'Facebook:'+(price_facebook)+'Snapchat:'+(price_snapchat)+'Amazon:'+(amazon_price)+'Apple:'+(apple_price)+'Walmart:'+(walmart_price))
    url = url + tweet
    response = requests.get(url)
    if response.status_code == 200:
        print("Tweet sent")
    else:
        print ("tweet failed due to error=")
        print (response.status_code)

    time.sleep(30)



