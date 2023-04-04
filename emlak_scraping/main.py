from prefect import flow, task
from prefect.blocks.system import Secret
from  emlak_scraping.emlak_scraping_modules.scrape_and_store import load_to_db
from emlak_scraping_modules.calculate_geo import calc_and_save
import emlak_scraping_modules.settings as set

@task(log_prints=True)
def refresh_primary_data(SCRAPING_DEPTH:int, REQUEST_DELAY:int, PROXY_URL:str ):
   load_to_db(SCRAPING_DEPTH, REQUEST_DELAY, PROXY_URL)

@task(log_prints=True)
def recalculate():
   calc_and_save()


@flow(name="Main Load", log_prints=True)
def main_task(SCRAPING_DEPTH:int = -1, REQUEST_DELAY:int =1):
   if set.NEED_PROXY:
      secret_block = Secret.load("proxy-url")   
      PROXY_URL=secret_block.get()
   refresh_primary_data(SCRAPING_DEPTH, REQUEST_DELAY, PROXY_URL)
   recalculate()

if __name__ == '__main__':
   main_task(3, 1)
      