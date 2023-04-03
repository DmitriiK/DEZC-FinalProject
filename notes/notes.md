az vm start -g rgMain -n dklmnUbuntu
az vm stop  -g rgMain -n dklmnUbuntu




 prefect orion start  # will start web UI

 proxy settings should be configured in prefect Secret block "proxy-url", 'http://<username>:<psw>@node-tr-2.astroproxy.com:11183'

 prefect deployment build ./main.py:main_task -n "Emlak Srappy"
  - will create emlak_scraping/main_task-deployment.yaml file, need to add parameters
then to deploy on server need to run:
 prefect deployment apply main_task-deployment.yaml

 need to run
 prefect agent start  --work-queue "default"
 (add nohup .. to make in running even when you close terminal )
 to run the deployment

 Metabase:
  - to make metabase available by external IP add inbound allow access rule for port 3000 for VM network interface