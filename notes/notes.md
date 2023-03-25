az vm start -g rgMain -n dklmnUbuntu
az vm stop  -g rgMain -n dklmnUbuntu




 prefect orion start  # will start web UI

 prefect deployment build ./main.py:main_task -n "Emlak Srappy"
  - will create emlak_scraping/main_task-deployment.yaml file, need to add parameters
then to deploy on server need to run:
 prefect deployment apply main_task-deployment.yaml

 need to run
 prefect agent start  --work-queue "default"
 to run the deployment

 Metabase:
  - to make metabase available by external IP add inbound allow access rule for port 3000 for VM network interface