from typing import Iterable, Tuple
import time
from itertools import product
from playwright.sync_api import sync_playwright
import json
import random

from metadata import JsonSchema, GetParams
import settings
import creds
# from datalake_store import AzureBlobFileUploader

baseURL = 'https://www.hepsiemlak.com/api/realty-list'

class scrapping_session:
    """
    SCRAPING_DEPTH      to restict scrapping depth, if minus one - without restirctions
    REQUEST_DELAY  seconds delay between requests
    """

    def __init__(self, SCRAPING_DEPTH: int = 999, MIN_REQUEST_DELAY: int = 1,  PROXY_URL: str = ''):
        self.SCRAPING_DEPTH = SCRAPING_DEPTH
        self.MIN_REQUEST_DELAY = MIN_REQUEST_DELAY
        self.last_request_time = None
        geoURLparts = settings.GEO_URL_PARTS
        self.start_urls = [f'{baseURL}/{x}&{y}&page=1' for x, y in product(
            geoURLparts, [GetParams.IsFurnished, GetParams.NotIsFurnished])]
        # https://www.hepsiemlak.com/antalya-kiralik-esyali?counties=kepez,konyaalti,muratpasa&furnishStatus=FURNISHED
        # https://www.hepsiemlak.com/api/realty-list/izmir-kiralik?furnishStatus=FURNISHED&page=1
        self.resp_content_size = 0  # responce content size
        self.pages_requested = 0
        self.items_parsed = 0
        if (settings.NEED_PROXY): # to do - figure out how to use proxy with playwright
            proxy_url = PROXY_URL if PROXY_URL else creds.PROXY_URL
            # self.session.proxies = {'http': proxy_url,    'https': proxy_url,   }

    def fetch_json(self, url: str, browser_page) -> Tuple[int, dict | None, str | None, int | None]:
        """
        Fetches JSON data from a GET API request using Playwright 

        Args:
            url: The URL of the API endpoint.

        Returns:
            A dictionary representing the JSON response, or None if an error occurs.
        """
        try:
            self.last_request_time = time.time()
            response = browser_page.goto(url)
            if response: 
                if response.ok:
                    content = response.text()
                    self.resp_content_size = + len(content)
                    self.pages_requested += 1
                    json_resp = json.loads(content)
                    next_page_url = None
                    totalPages, page = json_resp['totalPages'], json_resp['page']
                    if page < totalPages and (page <= self.SCRAPING_DEPTH or self.SCRAPING_DEPTH < 0):
                        # yes, I don't like it as well
                        next_page_url = url.replace(f'&page={page}', f'&page={page+1}')
                    return response.status, json_resp, next_page_url, page
                else:
                    print(f"Error fetching data from {url}: {response.status}")
                    return response.status, None, None, None       
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

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
                    key2 = int(
                        flds_down[1]) if flds_down[1].isdigit() else flds_down[1]
                    d_ret[key] = adv[flds_down[0]][key2]
            d_ret['is_furnished'] = GetParams.IsFurnished in url
            self.items_parsed += 1
            yield d_ret

    def make_random_delay(self) -> None:
        """# Introduce a random delay before making the request
        Args:
            min_delay (int, optional): _description_. Defaults to 1.
            max_delay (int, optional): _description_. Defaults to 2.
        """
        if self.last_request_time and self.MIN_REQUEST_DELAY:
            min_delay, max_delay = self.MIN_REQUEST_DELAY, self.MIN_REQUEST_DELAY + 2     
            delay = random.uniform(min_delay, max_delay)
            td = time.time() - self.last_request_time
            if td < delay:
                delay = delay - td
                print(f"Waiting for {delay:.2f} seconds before fetching ..")
                time.sleep(delay)

    def scrape(self) -> Iterable[dict]:
        with sync_playwright() as p:
            browser = p.firefox.launch()
            browser_page = browser.new_page()
            for start_url in self.start_urls:
                url = start_url
                # number_of_attempts = 0
                while (url):
                    print(f'url: {url}')
                    self.make_random_delay()
                    status, json_data, next_url, _  = self.fetch_json(url, browser_page)
                    if json_data :
                        for itm in self.parse_json(json_data, url):
                            yield itm
                        url = next_url
                    else:
                        # what should we yield here?
                        print(  f"Oops, something goes wrong,- for url: {url} we are getting status_code ={status}")
                    # number_of_attempts += 1

                    

if __name__ == '__main__':
    scrappy = scrapping_session()
    for itm in scrappy.scrape():
        continue
        print(itm)
    print(f'{scrappy.resp_content_size=}')
