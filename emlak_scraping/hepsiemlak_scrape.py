
import requests
import time
from  itertools import product

from metadata import JsonSchema, GetParams
import settings 
import creds
# baseURL = 'https://www.hepsiemlak.com/api/realty-list/'

class scrapping_session:
    def __init__(self):
        geoURLparts = [
            'izmir-kiralik?',  # Izmir
            'antalya-kiralik?counties=kepez,konyaalti,muratpasa&',  # Antalya
            'mersin-icel-kiralik-esyali?'  # Mersin
        ]

        self.start_urls = [f'https://www.hepsiemlak.com/api/realty-list/{x}&{y}&page=1' for x, y in product(geoURLparts, [GetParams.IsFurnished, GetParams.NotIsFurnished])]
        # https://www.hepsiemlak.com/antalya-kiralik-esyali?counties=kepez,konyaalti,muratpasa&furnishStatus=FURNISHED
        # https://www.hepsiemlak.com/api/realty-list/izmir-kiralik?furnishStatus=FURNISHED&page=1

        self.resp_content_size = 0 # responce content size
        self.pages_requested = 0
        self.items_parsed = 0
        self.session = requests.Session()
        if (settings.NEED_PROXY):
            if creds.PROXY_USER and creds.PROXY_PASSWORD:
                proxy_full_url = f'http://{creds.PROXY_USER}:{creds.PROXY_PASSWORD}@{settings.PROXY}'
                self.session.proxies = {
                    'http': proxy_full_url,
                    'https': proxy_full_url,
                }

    def request_api(self, url):
        self.pages_requested +=1
        r = self.session.get(url,  headers={'Accept': 'application/json'} ) # , verify=False
        json_resp, next_page_url = None, None
        if (r.status_code == 200):
            self.resp_content_size =+ len(r.content)
            json_resp = r.json()
            totalPages, page = json_resp['totalPages'], json_resp['page'] 
            if page < totalPages and page<=settings.SCRAPING_DEPTH:
                next_page_url = url.replace(f'&page={page}', f'&page={page+1}') # yes, I don't like it as well
        return r.status_code, json_resp, next_page_url


    def parse_json(self, json_resp, url):   
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
            self.items_parsed +=1
            yield d_ret

    def scrape(self):
        for start_url in self.start_urls:
            url = start_url
            number_of_attempts = 0
            while (url):
                print(f'url: {url}')
                number_of_attempts+=1
                status, json_data, next_url = self.request_api(url)
                if status == 200:
                    for itm in self.parse_json(json_data, url):
                        yield itm
                else:
                    print(f"Oops, something goes wrong,- for url: {url} we are getting status_code ={status}")
                    if (number_of_attempts < 10):
                        time.sleep(5)
                        continue
                    else:
                        return # todo: this will probably breake client.. need to do something more elegant                     

                time.sleep(settings.REQUEST_DELAY)
                url = next_url

if __name__ == '__main__':
   scrappy = scrapping_session()
   for itm in  scrappy.scrape():
       continue
       print(itm)
   print(f'{scrappy.resp_content_size=}')
