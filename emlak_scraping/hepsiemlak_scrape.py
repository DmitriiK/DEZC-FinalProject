
import requests
import time
from  itertools import product
from metadata import JsonSchema, GetParams
from settings import scraping_depth, request_delay
# baseURL = 'https://www.hepsiemlak.com/api/realty-list/'

geoURLparts = [
    'izmir-kiralik?',  # Izmir
    'antalya-kiralik?counties=kepez,konyaalti,muratpasa&',  # Antalya
    'mersin-icel-kiralik-esyali?'  # Mersin
]

start_urls = [f'https://www.hepsiemlak.com/api/realty-list/{x}&{y}&page=1' for x, y in product(geoURLparts, [GetParams.IsFurnished, GetParams.NotIsFurnished])]
# https://www.hepsiemlak.com/antalya-kiralik-esyali?counties=kepez,konyaalti,muratpasa&furnishStatus=FURNISHED
# https://www.hepsiemlak.com/api/realty-list/izmir-kiralik?furnishStatus=FURNISHED&page=1

def request_api(url):
    r = requests.get(url,  headers={'Accept': 'application/json'})
    json_resp, next_page_url = None, None
    if (r.status_code == 200):
        json_resp = r.json()
        totalPages, page = json_resp['totalPages'], json_resp['page'] 
        if page < totalPages and page<=scraping_depth:
            next_page_url = url.replace(f'&page={page}', f'&page={page+1}') # yes, I don't like it as well
    return r.status_code, json_resp, next_page_url


def parse_json(json_resp, url):   
    lst = json_resp[JsonSchema.rootNode]
    for adv in lst:
        d_ret = dict()
        for fld in JsonSchema.hepsiemlak_source_fields:
            flds_down = fld.split('/')
            key = JsonSchema.flat_name(fld)
            if len(flds_down) == 1:
                d_ret[key] = adv[flds_down[0]]
            else:
                key2 = int(flds_down[1]) if flds_down[1].isdigit() else flds_down[1]
                d_ret[key] = adv[flds_down[0]][key2]
        d_ret['is_furnished'] = GetParams.IsFurnished in url
        yield d_ret

def scrape():
    for start_url in start_urls:
        url = start_url
        number_of_attempts = 0
        while (url):
            print(f'url: {url}')
            number_of_attempts+=1
            status, json_data, next_url = request_api(url)
            if status == 200:
                for itm in parse_json(json_data, url):
                    yield itm
            else:
                  print(f"Oops, something goes wrong,- for url: {url} we are getting status_code ={status}")
                  if (number_of_attempts < 10):
                       time.sleep(5)
                       continue
                  else:
                      return # todo: this will probably breake client.. need to do something more elegant                     

            time.sleep(request_delay)
            url = next_url

if __name__ == '__main__':
   for itm in  scrape():
       continue
       print(itm)
