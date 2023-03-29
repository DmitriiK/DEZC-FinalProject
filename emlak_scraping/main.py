from prefect import flow, task

from  hepsiemlak_scrape import scrapping_session
from hepsiemlak_store import db_worker

@task(log_prints=True)
def load_to_db(SCRAPING_DEPTH:int, REQUEST_DELAY:int ):
   db = db_worker()
   db.init_load_session()
   scrappy = scrapping_session(SCRAPING_DEPTH = SCRAPING_DEPTH, REQUEST_DELAY= REQUEST_DELAY)
   for itm in scrappy.scrape():
      db.store_db(itm)
   print(f'{scrappy.items_parsed=}, {scrappy.pages_requested=}, {scrappy.resp_content_size=}')




@flow(name="Main Load", log_prints=True)
# @task(log_prints=True)
def main_task(SCRAPING_DEPTH:int = 999, REQUEST_DELAY:int =1):
   db = load_to_db(SCRAPING_DEPTH, REQUEST_DELAY)

if __name__ == '__main__':
   main_task(2, 1)
      