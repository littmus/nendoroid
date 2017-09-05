import types
import requests
from bs4 import BeautifulSoup as bs
import jsonpickle

jsonpickle.set_preferred_backend('simplejson')
jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

class Nendoroid(object):
    """docstring for Nendroid"""
    def __init__(self, link, icon):
        self.link = link
        self.photo_icon_src = icon

        self.num = 0
        self.name = ''
        self.name_jp = ''
        self.name_kr = ''
        self.name_en = ''
        self.series = ''
        self.manufacturer = ''
        self.category = ''
        self.sculptor = ''
        self.cooperation = ''
        self.isbn = ''
        self.price = 0
        self.photos_src = []

        self.products = []

    def __repr__(self):
        return 'No.{} {}'.format(self.num, self.name)

    def get_info(self):
        r = requests.get(self.link)
        soup = bs(r.text, "html.parser")

        info = soup.find('div', class_='itemInfo')
        self.num = info.find('div', class_='itemNum').text.strip()
        self.name = info.find('h1', class_='title').text.strip()
        
        #detail = soup.find('div', class_='itemDetail')

        box = soup.find('div', class_='detailBox').find('dl')
        values = box.find_all('dd')
        
        self.name_jp = values[0].text.strip()
        self.series = values[1].text.strip()
        self.manufacturer = values[2].text.strip()
        self.category = values[3].text.strip()
        self.price = int(values[4]['content'])
        self.sculptor = values[7].text.strip()
        self.cooperation = values[8].text.strip()

        # images
        photos = soup.find('div', class_='itemPhotos').find_all('img', class_='itemImg')
        #print(photos)
        self.photos_src = [p['src'] for p in photos]

        en_link = self.link.replace('ja/product', 'en/product')
        r = requests.get(en_link)
        soup = bs(r.text, "html.parser")

        info = soup.find('div', class_='itemInfo')
        self.name_en = info.find('h1', class_='title').text.strip()

    def to_str(self):
        return '{} {} {} {}'.format(self.num, self.name, self.name_kr, self.name_en)

    def to_json(self):
        json = jsonpickle.encode(self, unpicklable=False, make_refs=False)

        return json

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