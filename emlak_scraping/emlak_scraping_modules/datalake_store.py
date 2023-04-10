
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient
 ## shouldn't we leverage a azure-storage-file-datalake ? not sure what benefit it would give

DL_CONTAINER = "hepsiemlak"
 
class AzureBlobFileUploader:
  def __init__(self, bs_connections_string: str):
    self.init_data = datetime.now()
    self.blob_service_client =  BlobServiceClient.from_connection_string(bs_connections_string)
 
  def upload_content(self,content, blob_file_path):
    # Create blob with same name as local file name
    blob_client = self.blob_service_client.get_blob_client(container=DL_CONTAINER, blob=blob_file_path  )   
    try:
        blob_client.upload_blob(content, overwrite=True)
    except ValueError as err:
        logging.info("Error getting data from endpoint, %s", err)


 
if __name__ == '__main__':
   x = AzureBlobFileUploader()
   content='{"testkey":1}'
   x.upload_content(content=content,file_name = "testfolder/2022/12/01/antalya-kiralik?counties=kepez,konyaalti,muratpasa&/333.json")
      



