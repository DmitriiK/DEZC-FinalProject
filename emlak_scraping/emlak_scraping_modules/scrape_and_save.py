
from  hepsiemlak_scrape import scrapping_session
from hepsiemlak_store import db_worker

def load_to_db(SCRAPING_DEPTH:int, REQUEST_DELAY:int ):
   db = db_worker()
   db.init_load_session()
   scrappy = scrapping_session(SCRAPING_DEPTH = SCRAPING_DEPTH, REQUEST_DELAY= REQUEST_DELAY)
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
   load_to_db(3, 1)
      