import requests
from bs4 import BeautifulSoup as bs
from html5_parser import parse
import lxml

from nendoroid import Nendoroid
from nendoroid import Product
from market import Aladin, Amiami, AmazonJapan


jp_url = "http://www.goodsmile.info/ja/nendoroid{}-{}"
page_year = "http://www.goodsmile.info/ja/products/category/nendoroid_series/announced/{}"
s = requests.Session()

def parse_page(url):
    nendoroids = []
    r = s.get(url)
    tree = parse(r.content)
    items = tree.xpath('.//div[contains(@class, "hitItem")]')

    for item in items:
        if 'nendoroid' not in item.get('class').split():
            continue

        url = item.find('.//a').get('href')
        icon = item.find('.//img').get('data-original')

        nendo = Nendoroid(url, icon)
        try:
            nendo.get_info()
        except:
            continue
        else:
            nendoroids.append(nendo)

    return nendoroids

def main():
    aladin = Aladin()
    amiami = Amiami()
    #amazonjp = AmazonJapan()

    """
    for i in [7]:
        i,j = i*100, (i+1)*100
        if i != 0:
            i += 1
        else:
            i = '000'

        url = jp_url.format(i, j)
        print(url)
    """

    """
    for nendo in nendoroids:
        print(nendo)
        aladin_pr = aladin.get_product_info(nendo)
        if aladin_pr:
            nendo.products.append(aladin_pr)

        amiami_pr = amiami.get_product_info(nendo)
        if amiami_pr:
            nendo.products.append(amiami_pr)

        # isbn 없는 경우 검색을 제대로 할수가 없음..
        #amazon_pr = amazonjp.get_product_info(nendo)
        #if amazon_pr:
        #    nendo.products.append(amazon_pr)
    """
    with open("data/NendoroidData2.js", "wt", encoding='utf8') as data:
        data.write('var nendoroidMap = {\n')

        for year in range(2016, 2018):
            print(year)
            try:
                nendoroids = parse_page(page_year.format(year))
                nendo_data = ',\n'.join(['\"%s\":%s'%(nendo.num, nendo.to_json()) for nendo in nendoroids])
                data.write(nendo_data)
            except Exception as e:
                print(e.strerror)
                break

        data.write('\n};\n')

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
    """
if __name__ == '__main__':
    main()
