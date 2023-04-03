from prefect import flow, task
from prefect.blocks.system import Secret
from  emlak_scraping_modules.scrape_and_save import load_to_db
from emlak_scraping_modules.calculate_geo import calc_and_save
import emlak_scraping_modules.creds as cr
import emlak_scraping_modules.settings as set

@task(log_prints=True)
def refresh_primary_data(SCRAPING_DEPTH:int, REQUEST_DELAY:int ):
   load_to_db(SCRAPING_DEPTH, REQUEST_DELAY)

@task(log_prints=True)
def recalculate():
   calc_and_save()


@flow(name="Main Load", log_prints=True)
def main_task(SCRAPING_DEPTH:int = -1, REQUEST_DELAY:int =1):
   if set.NEED_PROXY:
      secret_block = Secret.load("proxy-url")   
      cr.PROXY_URL=secret_block.get()
   refresh_primary_data(SCRAPING_DEPTH, REQUEST_DELAY)
   recalculate()

if __name__ == '__main__':
   main_task(3, 1)
      