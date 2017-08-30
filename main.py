import requests
from bs4 import BeautifulSoup as bs
from nendoroid import Nendoroid
from nendoroid import Product
from market import Aladin, Amiami, AmazonJapan

import jsonpickle

jp_url = "http://www.goodsmile.info/ja/nendoroid{}-{}"

s = requests.Session()

def main():
    aladin = Aladin()
    amiami = Amiami()
    amazonjp = AmazonJapan()
    """
    for i in range(8):
        i,j = i*100, (i+1)*100
        if i != 0:
            i += 1
        else:
            i = '000'

        url = num_url.format(i, j)
        print(url)
        r = s.get(url)
        soup = bs(r.text)
        item = soup.find_all("div", class_='hitItem')
        print(len(item))
    """

    nen702 = Nendoroid.get_info('http://www.goodsmile.info/ja/product/6596/')
    print(nen702)
    j = jsonpickle.encode(nen702)
    print(j)
    print(nen702)
    rr = aladin.get_product_info(nen702)
    jr = jsonpickle.encode(rr)
    print(rr)
    print(jr)
    ami = amiami.get_product_info(nen702)
    print(ami)

    am = amazonjp.get_product_info(nen702)
    print(am)

if __name__ == '__main__':
    main()