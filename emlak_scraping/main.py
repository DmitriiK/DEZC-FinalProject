from prefect import flow, task
from prefect.blocks.system import Secret
# from prefect_azure import AzureBlobStorageCredentials

import emlak_scraping_modules.settings as sett
from  emlak_scraping_modules.scrape_and_store import load_to_db
from emlak_scraping_modules.calculate_geo import calc_and_save


@task(log_prints=True)
def refresh_primary_data(SCRAPING_DEPTH:int, REQUEST_DELAY:int, PROXY_URL:str, AZURE_BS_CS:str ='' ):
   load_to_db(SCRAPING_DEPTH, REQUEST_DELAY, PROXY_URL, AZURE_BS_CS)

@task(log_prints=True)
def recalculate():
   calc_and_save()


@flow(name="Main Load", log_prints=True)
def main_task(SCRAPING_DEPTH:int = -1, REQUEST_DELAY:int =1):
   PROXY_URL = ''
   AZURE_BS_CS=''
   if sett.NEED_PROXY:
      secret_block = Secret.load("proxy-url")  
      PROXY_URL= secret_block.get()
   if sett.SAVE_TO_BLOB_STORAGE:
      print('going to save raw data  to blob storage')
      secret_block = Secret.load("bscs-emlak") #  azure blob storage connection string
      AZURE_BS_CS = secret_block.get()
   refresh_primary_data(SCRAPING_DEPTH, REQUEST_DELAY, PROXY_URL,AZURE_BS_CS)
   recalculate()

if __name__ == '__main__':
   main_task(-1, 1)
      