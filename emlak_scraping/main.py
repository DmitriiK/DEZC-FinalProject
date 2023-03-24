from  hepsiemlak_scrape import scrapping_session
from hepsiemlak_store import save_to_db

if __name__ == '__main__':   
   scrappy = scrapping_session()
   db = save_to_db()
   for itm in scrappy.scrape():
      db.store_db(itm)
      