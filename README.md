# Aggregation of data on the cost of renting apartments in the cities of the Mediterranean coast of Turkey

## Objectives:
 - Create a datewarehouse for storing of data, related to realty market in Turkey
 - Create a system, that will refresh the data in this DW on periodic basis.
 - Calculate new geo-spatial attributes for realty objects in DWH, like "Distance to the sea cost" (Currently works for Antaly only)
 - Create dashboard for visualisation of the data in DWH
 - Usinig spatial interpolation, calculate a 2-D distibution  of prices of squre meter. The output of that process is some raster picture, that can be overlayed to Google Maps



### Technologies
## What technologies are being used?
- Cloud: [Azure Cloud](https://cloud.google.com)
- DWH: [Postres](https://www.postgresql.org/)
- Orchestration: [Prefect](https://www.prefect.io/)
- Data transformation: self made Python pipelines, leveraging Pandas and GeoPandas
- Data visualization and reporting: [Metabase](https://www.metabase.com/)
