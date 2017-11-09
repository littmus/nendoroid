import types
import requests
from html5_parser import parse
import lxml
import rapidjson
import jsonpickle

jsonpickle.load_backend('rapidjson')
jsonpickle.set_preferred_backend('rapidjson')
jsonpickle.set_encoder_options('rapidjson', skipkeys=True, indent=4, ensure_ascii=False, number_mode=rapidjson.NM_NATIVE)

#jsonpickle.set_preferred_backend('simplejson')
#jsonpickle.set_encoder_options('simplejson', ensure_ascii=False, sort_keys=True, indent=4)
class Nendoroid(object):
    """docstring for Nendroid"""

    attrs = {
        'price': '価格',
        'sculptor': '原型制作',
        'coop': '制作協力'
    }

    def __init__(self, link, icon):
        short_link = link.split('product/')[1]
        short_icon_src = icon.split('product/')[1]
        self.link = short_link
        self.photo_icon_src = short_icon_src

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
        tree = parse(r.content)
        self.num = tree.find('.//div[@class="itemNum"]//span').text.strip()
        self.name = tree.find('.//h1[@class="title"]').text.strip()
        print(self.num, self.name)

        detail = tree.find('.//div[@class="detailBox"]')
        attributes = [v.text.strip() if v.text is not None else '' for v in detail.iter('dt')]
        values = [v for v in detail.iter('dd')]

        self.name_jp = values[0].text.strip()
        self.series = values[1].text.strip()
        self.manufacturer = values[2].text.strip()
        #self.category = values[3].text.strip()
        #self.price = int(round(float(values[4].get('content'))))

        if self.attrs['price'] in attributes:
            idx = attributes.index(self.attrs['price'])
            try:
                self.price = int(round(float(values[idx].get('content'))))
            except:
                self.price = 0

        if self.attrs['sculptor'] in attributes:
            idx = attributes.index(self.attrs['sculptor'])
            self.sculptor = values[idx].text.strip()

        if self.attrs['coop'] in attributes:
            idx = attributes.index(self.attrs['coop'])
            self.cooperation = values[idx].text.strip()

        # images
        photos = tree.find('.//div[@class="itemPhotos"]//img[@class="itemImg"]')
        self.photos_src = [p['src'] for p in photos]

        en_link = self.link.replace('ja/product', 'en/product')
        r = requests.get(en_link)
        tree = parse(r.content)

        temp = tree.find('.//div[@class="itemInfo"]//h1[@class="title"]')
        if temp is not None:
            self.name_en = temp.text.strip()

    def to_str(self):
        return '{} {} {} {}'.format(self.num, self.name, self.name_kr, self.name_en)

    def to_json(self, mode=False):
        json = jsonpickle.encode(self, unpicklable=mode, make_refs=mode)

        return json

    @classmethod
    def from_json(j):
        pass

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
