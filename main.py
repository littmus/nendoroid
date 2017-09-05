import requests
from bs4 import BeautifulSoup as bs
from nendoroid import Nendoroid
from nendoroid import Product
from market import Aladin, Amiami, AmazonJapan


jp_url = "http://www.goodsmile.info/ja/nendoroid{}-{}"
page_2017 = "http://www.goodsmile.info/ja/products/category/nendoroid_series/announced/2017"
s = requests.Session()

def parse_page(url):
    nendoroids = []
    r = s.get(url)
    soup = bs(r.text, "html.parser")
    items = soup.find_all("div", class_='hitItem')
    print(len(items))

    for item in items[:5]:
        if 'nendoroid' not in item['class']:
            continue
        
        url = item.find('a')['href']
        icon = item.find('img')['data-original']

        nendo = Nendoroid(url, icon)
        nendo.get_info()
        nendoroids.append(nendo)
        
    return nendoroids

def main():
    aladin = Aladin()
    amiami = Amiami()
    amazonjp = AmazonJapan()
    
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
    nendoroids = parse_page(page_2017)
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
        #    nendo.products['AmazonJapan'] = amazon_pr

    with open("data/NendoroidData.js", "wt") as data:
        data.write('var nendoroidMap = {\n')
        nendo_data = ',\n'.join(['\"%s\":%s'%(nendo.num, nendo.to_json()) for nendo in nendoroids])
        data.write(nendo_data)
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