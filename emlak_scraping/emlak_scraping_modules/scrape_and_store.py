
from  hepsiemlak_scrape import scrapping_session
from hepsiemlak_dwh import db_worker

def load_to_db(SCRAPING_DEPTH:int, MIN_REQUEST_DELAY:int, PROXY_URL:str = ''):
   db = db_worker()
   db.init_load_session()
   scrappy = scrapping_session(SCRAPING_DEPTH = SCRAPING_DEPTH, MIN_REQUEST_DELAY= MIN_REQUEST_DELAY, PROXY_URL=PROXY_URL)
   status=0
   is_full= (SCRAPING_DEPTH<0 or SCRAPING_DEPTH>=999)
   try:
      for itm in scrappy.scrape():
         db.store_db(itm)
      print(f'{scrappy.items_parsed=}, {scrappy.pages_requested=}, {scrappy.resp_content_size=}')

      status =1
   except :
      status=-1
      raise
   finally: 
      db.close_session(items_processed=scrappy.items_parsed, status=status, is_full=is_full)



if __name__ == '__main__':
   load_to_db(10, 4)
      