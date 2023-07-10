
import requests
import time
from  itertools import product
import json
from metadata import JsonSchema, GetParams
import settings 
import creds
from datalake_store import AzureBlobFileUploader
baseURL = 'https://www.hepsiemlak.com/api/realty-list'


class scrapping_session:
    """
    SCRAPING_DEPTH      to restict scrapping depth, if minus one - without restirctions
    REQUEST_DELAY  seconds delay between requests
    """

    def __init__(self, SCRAPING_DEPTH:int = 999, REQUEST_DELAY:int = 1,  PROXY_URL:str = '',  AZURE_BS_CS:str =''):
        self.SCRAPING_DEPTH = SCRAPING_DEPTH
        self.REQUEST_DELAY = REQUEST_DELAY
        geoURLparts = settings.GEO_URL_PARTS
        self.start_urls = [f'{baseURL}/{x}&{y}&page=1' for x, y in product(geoURLparts, [GetParams.IsFurnished, GetParams.NotIsFurnished])]
        # https://www.hepsiemlak.com/antalya-kiralik-esyali?counties=kepez,konyaalti,muratpasa&furnishStatus=FURNISHED
        # https://www.hepsiemlak.com/api/realty-list/izmir-kiralik?furnishStatus=FURNISHED&page=1

        if settings.SAVE_TO_BLOB_STORAGE:
            bs_cs = AZURE_BS_CS or creds.BLOB_STORAGE_CONNECTION_STRING
            self.blob_sink = AzureBlobFileUploader(bs_cs)

        self.resp_content_size = 0 # responce content size
        self.pages_requested = 0
        self.items_parsed = 0
        self.session = requests.Session()
        if (settings.NEED_PROXY):
            proxy_url = PROXY_URL if  PROXY_URL else creds.PROXY_URL
            self.session.proxies = {
                'http': proxy_url,
                'https': proxy_url,
            }

    def request_api(self, url):
        self.pages_requested +=1
        headers = {'Accept': 'application/json'
                   ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'} 

        r = self.session.get(url,  headers=headers ) # , verify=False
        json_resp, next_page_url,page = None, None, None
        if (r.status_code == 200):
            self.resp_content_size =+ len(r.content)
            json_resp = r.json()
            totalPages, page = json_resp['totalPages'], json_resp['page'] 
            if page < totalPages and (page<=self.SCRAPING_DEPTH or self.SCRAPING_DEPTH<0):
                next_page_url = url.replace(f'&page={page}', f'&page={page+1}') # yes, I don't like it as well
        return r.status_code, json_resp, next_page_url, page


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
                status, json_data, next_url,page = self.request_api(url)
                if status == 200:
                    self.save_to_blob(json_data, url, page)
                    for itm in self.parse_json(json_data, url):
                        yield itm
                else:
                    print(f"Oops, something goes wrong,- for url: {url} we are getting status_code ={status}")
                    if (number_of_attempts < 10):
                        time.sleep(5)
                        continue
                    else:
                        return # todo: this will probably breake client.. need to do something more elegant                     

                time.sleep(self.REQUEST_DELAY)
                url = next_url

    def save_to_blob(self,json_data:str, url:str, page:int):
        if not settings.SAVE_TO_BLOB_STORAGE:
            return
        if not self.blob_sink:
            self.blob_sink = AzureBlobFileUploader()
        bs_init_data = self.blob_sink.init_data
        geo_part = [x for x in settings.GEO_URL_PARTS if x in url][0] #something wrong with this implementation..
        blob_file_path = f'{bs_init_data.year}/{bs_init_data.month}/{bs_init_data.day}/{geo_part}/{page}.json'
        json_str = json.dumps(json_data, indent=4, ensure_ascii=False)
        self.blob_sink.upload_content(blob_file_path=blob_file_path, content=json_str)




if __name__ == '__main__':
   scrappy = scrapping_session()
   for itm in  scrappy.scrape():
       continue
       print(itm)
   print(f'{scrappy.resp_content_size=}')
