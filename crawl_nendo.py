import requests
from bs4 import BeautifulSoup as bs
from html5_parser import parse
import lxml

from nendoroid import Nendoroid

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
    with open("data/NendoroidData2.js", "wt", encoding='utf8') as data:
        data.write('var nendoroidMap = \n{\n')

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

if __name__ == '__main__':
    main()
