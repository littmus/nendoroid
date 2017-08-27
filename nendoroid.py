import types
import requests
from bs4 import BeautifulSoup as bs

class Nendoroid(object):
    """docstring for Nendroid"""
    def __init__(self):
        self.num = 0
        self.name = ''
        self.name_kor = ''
        self.name_eng = ''
        self.series = ''
        self.manufacturer = ''
        self.category = ''
        self.isbn = ''

        self.products = []

    def __repr__(self):
        return 'No.{} {}'.format(self.num, self.name)

    def get_info(link):
        r = requests.get(link)
        soup = bs(r.text, "html.parser")
        
        num = int(soup.find('div', class_='itemNum').text)
        name = soup.find('h1', class_='title').text.strip()
        box = soup.find('div', class_='detailBox').find('dl')
        values = box.find_all('dd')
        
        series = values[1].text.strip()
        manufacturer = values[2].text.strip()
        category = values[3].text.strip()
        price = int(values[4]['content'])

        nendo = Nendoroid()
        nendo.num = num
        nendo.name = name
        nendo.series = series
        nendo.manufacturer = manufacturer
        nendo.category = category

        return nendo

class Product(object):

    def __init__(self, nendroid, market, link, base_price, discount=None, mileage=None):
        self.nendroid = nendroid
        self.market = market
        self.price = base_price
        self.link = link

        if isinstance(discount, types.FunctionType):
            discount_amount = discount(self.price)
        elif isinstance(discount, int):
            discount_amount = discount
        else:
            discount_amount = 0

        for k in market.discounts:
            discount_func = market.discounts[k]
            discount_amount += discount_func(self.price)

        self.discounted_price = self.price - discount_amount

        if market.name == '알라딘':
            self.exchanged_price = self.discounted_price
        else:
            self.exchanged_price = self.discounted_price * 11

        if isinstance(mileage, types.FunctionType):
            self.mileage = mileage(self.discounted_price)
        elif isinstance(mileage, int):
            self.mileage = mileage
        else:
            self.mileage = 0

        for k in market.mileages:
            mileage_func = market.mileages[k]
            self.mileage += mileage_func(self.discounted_price)

    def __repr__(self):
        return '{} - {} : {} -> {} / {}'.format(self.nendroid, self.market, self.price, self.discounted_price, self.mileage)