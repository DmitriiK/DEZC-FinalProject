# Aggregation of data on the cost of renting of apartments in the cities of the Mediterranean coast of Turkey
![image](https://user-images.githubusercontent.com/20965831/229925996-f877ad63-d7dd-4bc9-9794-7282270faa82.png)



## Objectives:
 - Create a date-warehouse for storing of data, related to realty market in Turkey
 - Create a system, that will refresh the data in this DWH on a periodic basis.
 - Calculate new geospatial attributes for realty objects in DWH, like "Distance to the sea cost" (Currently works for Antaly only)
 - Create dashboard for visualisation of the data in DWH
 - Using spatial interpolation, calculate a 2-D distribution  of prices. The output of that process is a raster picture, that can be overlayed to Google Maps


## What technologies are being used?
- Cloud: [Azure Cloud](https://cloud.google.com)
- Containerization [Docker](https://www.docker.com)
- Blob storage, Data lake architecture (https://azure.microsoft.com/en-us/products/storage/blobs)
- DWH: [Postres](https://www.postgresql.org/)
- Orchestration: [Prefect](https://www.prefect.io/)
- Data transformation: self made Python pipelines, leveraging [Pandas](https://pandas.pydata.org/) and [GeoPandas](https://geopandas.org)
- Data visualization and reporting: [Metabase](https://www.metabase.com/)
- [Spatial interpolation using IDW](https://gisgeography.com/inverse-distance-weighting-idw-interpolation/) - Initial idea was taken from [Jack Kaufman publication](https://www.jefftk.com/p/updated-boston-apartment-price-maps)

## DWH database schema
![image](https://user-images.githubusercontent.com/20965831/230159798-368ed399-b085-4c74-abb7-f97551642be1.png)


## Data sources:
- [Hepsiemlak](https://www.hepsiemlak.com/) - Turkish site with ads with realy objects, sell and rent.
- Files with geospatial data, Mediterranean Sea borders, polygons with administrative districts in Turkey.


## Currently it works like this:
![image](https://user-images.githubusercontent.com/20965831/229867093-2f5571a2-49bc-4d36-a0c7-0339d612a0a0.png)

- Python pipeline scrapes data from some API, provided by [Hepsiemlak](https://www.hepsiemlak.com/), loads that data to kind of DWS (simple star schema in of Postgres). Note: when running this pipeline form the locations outsdide Turkey, need to use Turksih proxy.
Optionally you can attach a functinality to save a content of API responce to kind of Data Lake in Azure Blob Storage
- Another python script calculates distance to the sea, using spatial files with  Mediterranan Sea borders, leveraging GeoPandas (currenlty works for Antalya only).
(the work of these 2 pipelines is orchestrated by Prefect)
- Another pythoh script uses that data for spatial intrerpolation calculations. An output of this process is raster image file. It should be copied to some static site, where we can overlay it on Google Maps. Final result of that process looks like this.(Currenlty this step is done manually)
 - For creation of dashboards for end user I levarage Metabase.


## Repository organization
-  [deployment](deployment/README.md):
    &ensp;&thinsp; Docker files and prefect deployment file, and file with deployment and setup desciption
 - [emlak_scraping](emlak_scraping/README.md): main python code for scraping, parsing, loading to DWH and geo-calculations
 -  [metabase](metabase) - just postgres backup of my metabase (unfortunately, free version of Metabase does not allow to export/import metadata)
 -  [SQL](SQL) : database schema and stored procedures for DWH

## Results
- [Dashboard for all cities](http://dklmn.westeurope.cloudapp.azure.com:3000/public/dashboard/036832b6-da5d-4da8-b1e4-c2720926d01e?room_category=2%2B1&room_category=1%2B1&room_category=3%2B1&room_category=4%2B1&age_or_buiding_is_less_than=100)

![image](https://user-images.githubusercontent.com/20965831/229874671-cb6bca21-ef77-43cb-b83a-9af48d512043.png)
 &ensp;&thinsp;
 
- [Dashboard with detailed information for Antalya](http://dklmn.westeurope.cloudapp.azure.com:3000/public/dashboard/57630ab3-a557-4e3b-a081-2beb2dc2da93?room_category=1%2B1&room_category=2%2B1&room_category=3%2B1&room_category=4%2B1&distance_to_see_within.._km=30&number_of_floors_in_the_building=1&number_of_floors_in_the_building=10)  
Note: dashboards from the links above might be unavailable, as I might switch off the VM to save some money..
![image](https://user-images.githubusercontent.com/20965831/229874237-028dc808-3fd5-482b-8272-db36e89a8bf8.png)  

 - Web pages with results of spatial interpolation
 [Antalya rent prices spatial distributions.](https://dmitriik.github.io/RealtyEstimation/Antalya/)
![image](https://user-images.githubusercontent.com/20965831/229874912-acdd7cd4-684b-432f-a618-340ba612b04d.png)

## In my future plans
- Functional requirements
  - Apply multiple regression calculation for creation of some statisctical models
  - And a filter, that will allow to show on "most attractive proposals" using this model
  - Create a Telegram chat bot, that will send such proposals, using the requirements, given by user
  - Create separate dashboards for all cities.
  -  Add more sities to processing
  -  Make colored map of price distributions, using division by Mahalle (small city region in Turkey)

- Non functional requirements
  - Perfomance of dashboard rendering. Currently it works bit slowly. Need to investigate what can be done on database level, maybe it would make sence to leverage column store indexes or leverage caching in Metabase
  - Perform some refactoring of the code
  - Polish litle bit the appearance of dashboards
  - Investigate does it worth trying another open source BI tools, like Apache Superset.



    
