import math
import json
import requests
from bs4 import BeautifulSoup as bs
import bottlenose

import config
from nendoroid import Product

class Market(object):
    def __init__(self, name, discounts={}, mileages={}, shipping_fee=None):
        self.name = name
        self.discounts = discounts
        self.mileages = mileages
        self.shipping_fee = shipping_fee

    def __repr__(self):
        return self.name

class AmazonJapan(Market):

    def __init__(self):
        discounts = {}
        discounts['소비세'] = lambda price:math.ceil(price*0.074)
        shipping_fee = {
            'Standard':lambda n:n*250 + 400,
            'Priority':lambda n:n*500 + 600
        }
        super().__init__('일마존', discounts)

        self.amazon = bottlenose.Amazon(
            config.AMAZON_ACCESS_KEY, config.AMAZON_SECRET_KEY, config.AMAZON_JP_ASSOCIATE_TAG, Region="JP",
            Parser=lambda text:bs(text, "lxml")
        )

    def get_product_info(self, nendoroid):
        r = self.amazon.ItemSearch(Keywords=nendoroid.isbn, SearchIndex="Hobbies")
        
        asin = r.find('asin').string
        link = r.find('detailpageurl').string
        
        r = self.amazon.ItemLookup(ItemId=asin, ResponseGroup='Offers')
        amazon_offer = r.find('offer')
        price = int(amazon_offer.find('price').find('amount').string)
        saved = int(amazon_offer.find('amountsaved').find('amount').string)
        
        product = Product(nendoroid, self, link, price, discount=saved)
        
        return product


class Amiami(Market):
    search_url = 'http://slist.amiami.com/top/search/list'
    search_params = {
        's_keywords':''
    }
    shipping_fee_table = {
        'ASP':[980, 1480, 1920, 2360],
        'EMS':[1400, 2100, 2700, 3300, 3800, 4300, 5300, 5300, 6300, 6300, 7300, 7300, 8100, 8100, 8900, 8900, 9700, 9700, 10500, 10500],
        'DHL':[-1, 2200, 2650],
    }
    def __init__(self):
        mileages = {}
        mileages['기본 마일리지'] = lambda price:math.ceil(price*0.01)
        shipping_fee = {
            'ASP':lambda n:self.shipping_fee_table['ASP'][n-1] if n <= 4 else -1,
            'EMS':lambda n:self.shipping_fee_table['EMS'][n-1] if n <= 20 else -1,
            'DHL':lambda n:self.shipping_fee_table['DHL'][n-1] if n <= 20 else -1,
        }
        super().__init__('아미아미', {}, mileages)

    def get_product_info(self, nendoroid):
        self.search_params['s_keywords'] = nendoroid.isbn
        r = requests.get(self.search_url, params=self.search_params)
        
        soup = bs(r.text, "html.parser")
        table = soup.find('table', class_='product_table')
        item = table.find_all('td', class_='product_box')

        if item:
            item = item[0]
            link = item.find('a')['href']

            r = requests.get(link)
            soup = bs(r.text, "html.parser")
            selling_price = soup.find('li', class_='selling_price').text.strip().split()[0]
            selling_price = int(selling_price.replace(',', ''))

            off_price_per = soup.find('span', class_='off_price').text.strip().split('%')[0]
            off_price_per = float(off_price_per) * 0.01
            off_price = lambda price:math.ceil(price*off_price_per/10)*10

            product = Product(nendoroid, self, link, selling_price, discount=off_price)
            return product

        else:
            return None

class Aladin(Market):
    
    search_url = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
    search_params = {
        'TTBKey':config.ALADIN_KEY,
        'QueryType':'Title',
        'SearchTarget':'Foreign',
        'Output':'JS',
    }

    def __init__(self):     
        discounts = {}
        #discounts['기본 할인'] = lambda price:math.ceil((price*0.1/10))*10
        discounts['5만원 이상 할인'] = lambda price:2000 if price >= 50000 else 0
        
        mileages = {}
        mileages['5만원 이상 마일리지 '] = lambda price:2000 if price >= 50000 else 0
        #mileages['상품 마일리지'] = lambda price:price*0.03

        super().__init__('알라딘', discounts, mileages)

    def get_product_info(self, nendoroid):
        self.search_params['Query'] = nendoroid.name
        r = requests.get(self.search_url, params=self.search_params)
        res = json.loads(r.text[:-1])
        item = res['item']

        if item:
            item = item[0]
            link = item['link']
            price = int(item['priceSales'])
            mileage = int(item['mileage'])
            isbn = item['isbn13']

            nendoroid.isbn = isbn
            nendoroid.name_kor = item['title'].split('(')[0]
            product = Product(nendoroid, self, link, price, mileage=mileage)

            return product
        else:
            return None

class Goodsmile(Market):
    def __init__(self):
        shipping_fee = 2000
        pass

    def get_product_info(self, nendoroid):

        product = Product(nendoroid, )



class AmazonUSA(Market):
    def __init__(self):
        pass

class Mandarake(Market):
    def __init__(self):
        pass

class Surugaya(Market):
    def __init__(self):
        pass