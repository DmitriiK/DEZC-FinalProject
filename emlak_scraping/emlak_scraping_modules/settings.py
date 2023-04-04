SQL_HOST = 'localhost'
SQL_DB = 'emlak'

NEED_PROXY = 1
PROXY = 'node-tr-2.astroproxy.com:11183'

GEO_URL_PARTS = [
            'izmir-kiralik?',  # Izmir
            'antalya-kiralik?counties=kepez,konyaalti,muratpasa&',  # Antalya
            'mersin-icel-kiralik-esyali?'  # Mersin
        ]

MEDITERRANEAN_SEA_GEO_FILE = '/home/dklmn/code/DEZC-FinalProject/emlak_scraping/geo_data/iho.zip' # file path to geo shape file with sea
SPATIAL_INTERPOLATION_SITE_PATH ='/home/dklmn/code/DmitriiK.github.io/RealtyEstimation/' # Path to output folder for spatial interpolation calculations
