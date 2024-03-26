import time
from bs4 import BeautifulSoup as bs
import requests
import json
from unidecode import unidecode
import selenium.webdriver

def getCookiesFromSite(url: str = None):
    if url is None:
        print("No url given")
        return None
    # headless browser to get cookies
    with open('cookies.json') as f:
        cookies = json.load(f)
        expiry = 999999999999999999999
        for cookie in cookies:
            if cookie["expiry"] < expiry:
                expiry = cookie["expiry"]
    
    if expiry > int(time.time()):
        cookiestring = ""
        for cookie in cookies:
            cookiestring += cookie["name"] + "=" + cookie["value"] + "; "
        return cookiestring
    options = selenium.webdriver.ChromeOptions()

    options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
    options.add_argument("--headless")

    driver = selenium.webdriver.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get(url)
    cookies = driver.get_cookies()
    driver.quit()
    cookiestring = ""
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)
    for cookie in cookies:
        cookiestring += cookie["name"] + "=" + cookie["value"] + "; "
    return cookiestring

def getProxies():
    with open('http_proxies.json') as f:
        proxieslist = json.load(f)
        proxiess = proxieslist["proxies"]
        proxies = {"http": [], "https": []}
        for proxy in proxiess:
            proxies["http"].append("http://" + proxy)
            proxies["https"].append("http://" + proxy)
    return proxies

def getHeaders():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': 'ssa-did=bce29e6e-c97b-463e-addd-1def62875db0; uid=1469684; __Secure-TnetID=0_dIs62X8xuQG68KMvACRhO6u6F9tybq; twk-theme=twk-dark; SSLB=1; SSID=CQBXER0OACgAAACMo3NjLEDAAIyjc2NYAAAAAAAAAAAAyBTOZQDQnCABAAHvKwAAyBTOZQEA6AAAAOsAAADLAAAA8wAAALMAAAANAQAAEAEAABMBAAAUAQAAGQEAAA; SSSC=2.G7166251253779939372.88|288.11247; SSRT=yBTOZQADAA; ssa-sid=018dad01-3527-7976-b96b-6bf2f5db65b1; tc=1708004582%2C1708004581; SSOD=ADumAAAANgDhDQAAZQEAAIyjc2PmFM5lQABNDgAAvgIAAIyjc2PmFM5lQwDTHQAAHAAAAEca9mMZ_6dlAAAAAA; SSPV=D1QAAAAAAIQAAAAAAAAAAAAAAEAAAAAAAAAAAAAA; tbb=false',

    }
    headers["cookie"] = getCookiesFromSite("https://tweakers.net")
    return headers

def getProductpage(product: str = None, proxies = None):
    if product is None:
        print("No product given")
        return None
    url = 'https://tweakers.net/ajax/zoeken/pricewatch/?keyword=' + \
        product + '&output=json&country=BE'
    if proxies is not None:
        data = requests.get(url, proxies=proxies).json()
    else:
        data = requests.get(url).json()
    return data["articles"][0]["link"]

def getProductSpecs(url: str = None, product: str = None, proxies = None):
    if url is None and product is None:
        print("No url or product given")
        return None
    if proxies is None:
        data = requests.get(url + "/specificaties", headers=getHeaders()).text
    else:
        data = requests.get(url + "/specificaties", proxies=proxies).text
    soup = bs(data, 'html.parser')
    try:
        if "Sorry, je gaat even iets te snel" in soup.find_all('h1')[1].text.strip():
            raise Exception("Too many requests, we are being rate limited. Try again later.")
    except:
        pass     
    specs = soup.find_all('td', {'class': 'spec'})
    speclabels = soup.find_all('td', {'class': 'spec-label'})
    speclabels = [label.text.strip() for label in speclabels]
    specs = [spec.text.strip() for spec in specs]
    specdict = {}
    for i in range(len(speclabels)):
        specdict[speclabels[i]] = specs[i]
    return specdict
    


#print(getProductpage("iphone 11 128gb"))
def getPrices(url: str = None, proxies = None):
    if url is None:
        print("No url given")
        return None
    if proxies is None:
        data = requests.get(url).text
    else:
        data = requests.get(url, proxies=proxies).text
    soup = bs(data, 'html.parser')
    try:
        if "Sorry, je gaat even iets te snel" in soup.find_all('h1')[1].text.strip():
            raise Exception("Too many requests, we are being rate limited. Try again later.")  
    except:
        pass

    table = soup.find_all('table', {'class': 'shop-listing'})
    shops = table[0].find_all('tr')
    for i in range(len(table)):
        print(len(table[i].find_all('tr')))
        # get the table with the most shops
        if "refurbished" not in table[i].find_all('tr'):
            if len(table[i].find_all('tr')) > len(table[i-1].find_all('tr')):
                shops = table[i].find_all('tr')
    print(len(shops))

    productname = soup.find('h1').text.strip()

    items = {"items": []}
    items["name"] = productname
    countr = 0
    for shop in shops:
        shop_name = shop.find('td', {'class': 'shop-name'})
        shop_url = shop_name.find('a').get('href')
        shop_name = shop_name.find('a').text.strip()
        shop_name = unidecode(shop_name)

        shop_price = shop.find('td', {'class': 'shop-price'})
        shop_price = shop_price.find('a').text.strip().replace(
            ",-", "").replace("€", "").replace(" ", "").replace("\xa0", "")
        if "." in shop_price:
            shop_price = float(shop_price.split(".")[0] + "" + shop_price.split(".")[1].replace(",", "."))
        elif "," in shop_price:
            shop_price = float(shop_price.replace(",", "."))

        items["items"].append({
            "shop": shop_name,
            "price": shop_price,
            "url": shop_url
        })
    # sort by price
    items["items"] = sorted(items["items"], key=lambda k: float(k['price']))
    return items


def getAveragePrice(prices: list = None):
    """Returns the average price of a list of stores and their prices"""
    if prices is None:
        print("No prices given")
        return None
    total = 0
    for price in prices:
        total += float(price["price"])
    return round(float(total / len(prices)), 2)


def getMedianPrice(prices: list = None):
    """Returns the median price of a list of stores and their prices"""
    if prices is None:
        print("No prices given")
        return None
    prices = sorted(prices, key=lambda k: float(k['price']))
    return round(float(prices[int(len(prices)/2)]["price"]), 2)