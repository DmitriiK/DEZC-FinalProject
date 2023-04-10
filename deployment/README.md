#  Deployment process (Ubuntu)

- Initial infrastructure setup.
  (You can follow the steps from 
  [DE Zoomcamp 1.4.1 - Setting up the Environment on Google Cloud (Cloud VM + SSH access)](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb))

  - Generating SSH keys
  - Creating a virtual machine on the cloud (Azure ubuntu 20.04 Standard B2s (2 vcpus, 4 GiB memory)ry) for my case)
  - Connecting to the VM with SSH
  - Installing Anaconda (if you are going to go with it)
  - Installing Docker
  - Creating SSH config file
  - Accessing the remote machine with VS Code and SSH remote
  - Installing docker-compose
  
- Make git clone for this repository in the appropriate folder
- Make an environment and activate it, for conda you can use commands 
  - _conda create --name zoomcamp_
  - _conda activate zoomcamp_
- Install necessary dependencies using 
  - _pip install -r requirements.txt_  
  from emlak_scraping folder.
- Using VS code terminal(needed for correct mapping of remote ports to local dev machine), start prefect UI using command 
  - _prefect orion start_   
  It will start web UI for prefect.
- If you need some proxy server (and you will need it if you are outside Turkey) go to the blocks section of Prefect UI
and create 'proxy-url' key in the "Secrets" block. URL might look like this - 'http://<user>:<psw>@node-tr-2.astroproxy.com:11183'
- Go to the docker folder and spin up Postgres and Metabase inside docker, using command 
  - _docker-compose up_  
  (you can change some parameters as ports and postgres credential inside docker-compose.yaml file)
- Ensure in VS code terminal, that you for all guys (Postgres, Metabase, Prefect, pgadmin (last one is optional) ) - we have the ports appropriately forwarded.
- Using Posgres client (I am using [DBVeaver](https://dbeaver.io/)) make a connection to the postgres server, yo have launched. 
You should consider the parameters from the docker compose file from the prev step.
Take the dump file from metabase folder  and restore it to Postgres server. This will create necessary models and dashboard in metabase
  (Unfortunately free version of Metabase does not support import export)
- If you are goint go levarage saving of json response to blob storage, create Azure blob storage account and container for it, using either terraform templates here or manually, and set the correspondent values of settings.py file to try. You should also provide connection string after that, either write it to creds.py file, or apply it as Prefect Secret Block
- Reassign some environment-specific values in \emlak_scraping_modules\settings.py and creds.py. 
 You can also change here parameter GEO_URL_PARTS, which affects the initial pages for scraping. 
 - Check Postgres database with the name, specified in settings.SQL_DB parameter and in docker-compose file, (emlak). 
 Run on this DB the scripts for creation of tables, SP-s and views from SQL folder.
 - If you want to store scraped data not only in DWH storage, but in the Azure Blob Storage as well, need to 
assign the values settings.SAVE_TO_BLOB_STORAGE and creds.BLOB_STORAGE_CONNECTION_STRING.

- Run the emlak_scraping\main.py script. You can use default parameters, SCRAPING_DEPTH:int = -1, REQUEST_DELAY:int =1. 
It will mean that scraping module will parse all pages up to the end, using 1 seconds delay between each get request
Check, if  data has appeared in the appropriate tables, and the result of flow runs are visible in Prefect UI in the Flow Runs.
- Check the work of Metabase models, questions, and dashboards.
- If everything is OK,check content main_task-deployment.yaml file, change default values if needed, 
   and deploy existing "deployment file " to Prefect using command like this:
  - _prefect deployment apply main_task-deployment.yaml_
- create a schedule for this deployment
- run
  - _prefect agent start  --work-queue "default"_  
  check that our flow will start in the time, defined in you prefect deployment schedule.
- for creation of raster file with spatial interpolation need to run _emlak_scraping\draw_spatial\draw_heatmap.py_ module for 
each of the cities (Antalya, Izmir, Mersin). Currently the resulting file should be manually loaded to another gir repository
  [FE part for spatial interpolation](https://github.com/DmitriiK/DmitriiK.github.io)

  


