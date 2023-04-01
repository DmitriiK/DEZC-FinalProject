from prefect import flow, task

from  hepsiemlak_scrape import scrapping_session
from hepsiemlak_store import db_worker
from calculate_geo import calc_and_save

@task(log_prints=True)
def load_to_db(SCRAPING_DEPTH:int, REQUEST_DELAY:int ):
   db = db_worker()
   db.init_load_session()
   scrappy = scrapping_session(SCRAPING_DEPTH = SCRAPING_DEPTH, REQUEST_DELAY= REQUEST_DELAY)
   status=0
   try:
      for itm in scrappy.scrape():
         db.store_db(itm)
      print(f'{scrappy.items_parsed=}, {scrappy.pages_requested=}, {scrappy.resp_content_size=}')
      is_full= (SCRAPING_DEPTH<0 or SCRAPING_DEPTH>=999)
      status =1
   except :
      status=-1
      raise
   finally: 
      db.close_session(items_processed=scrappy.items_parsed, status=status, is_full=is_full)

@task(log_prints=True)
def recalculate():
   calc_and_save()




@flow(name="Main Load", log_prints=True)
def main_task(SCRAPING_DEPTH:int = 999, REQUEST_DELAY:int =1):
   load_to_db(SCRAPING_DEPTH, REQUEST_DELAY)
   calc_and_save()

if __name__ == '__main__':
   main_task(-1, 1)
      