import hepsiemlak_scrape
from hepsiemlak_store import save_to_db

if __name__ == '__main__':
   db = save_to_db()
   for itm in hepsiemlak_scrape.scrape():
      db.store_db(itm)
      