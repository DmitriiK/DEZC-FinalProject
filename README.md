# Aggregation of data on the cost of renting of apartments in the cities of the Mediterranean coast of Turkey



## Objectives:
 - Create a datewarehouse for storing of data, related to realty market in Turkey
 - Create a system, that will refresh the data in this DW on periodic basis.
 - Calculate new geospatial attributes for realty objects in DWH, like "Distance to the sea cost" (Currently works for Antaly only)
 - Create dashboard for visualisation of the data in DWH
 - Using of  spatial interpolation, calculate a 2-D distribution  of prices of square meter. The output of that process is some raster picture, that can be overlayed to Google Maps


## What technologies are being used?
- Cloud: [Azure Cloud](https://cloud.google.com)
- Containerization [Docker](https://www.docker.com
)
- DWH: [Postres](https://www.postgresql.org/)
- Orchestration: [Prefect](https://www.prefect.io/)
- Data transformation: self made Python pipelines, leveraging [Pandas](https://pandas.pydata.org/) and [GeoPandas](https://geopandas.org)
- Data visualization and reporting: [Metabase](https://www.metabase.com/)
- [Spatial interpolation using IDW](https://gisgeography.com/inverse-distance-weighting-idw-interpolation/) - Initial idea was taken from [Jack Kaufman publication](https://www.jefftk.com/p/updated-boston-apartment-price-maps)

## Data sources:
- [Hepsiemlak](https://www.hepsiemlak.com/) - Turkish site with ads with realy objects, sell and rent.
- Files with geospatial data, Mediterranean Sea borders, polygons with administrative districts in Turkey.

## Repository organization
- deployment:
    &ensp;&thinsp; Docker files and prefect deployment file
 - [emlak_scraping](emlak_scraping/README.md): main python code for scraping, parsing, loading to DWH and geo-calculations
 -  metabase - just postgres backup of my metabase (unfortunately, free version of Metabase does not allow to export/import metadata)
 -  SQL : database schema and stored procedures for DWH
    