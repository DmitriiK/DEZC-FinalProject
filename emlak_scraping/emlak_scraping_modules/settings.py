SQL_HOST = 'localhost'
SQL_DB = 'emlak'
SQL_PORT=5432

NEED_PROXY = 1
PROXY = 'node-tr-2.astroproxy.com:11183'

GEO_URL_PARTS = [
            'izmir-kiralik?subCategories=residence,daire',  # Izmir
            'antalya-kiralik?subCategories=daire,residence&counties=antalya-aksu,alanya,dosemealti,antalya-kemer,kepez,konyaalti,manavgat,muratpasa',  # Antalya
            'mersin-icel-kiralik-esyali?subCategories=daire,residence'  # Mersin
            ,'isparta-kiralik?subCategories=daire,residence'
        ]

MEDITERRANEAN_SEA_GEO_FILE = '/home/dklmn/code/DEZC-FinalProject/emlak_scraping/geo_data/iho.zip' # file path to geo shape file with sea
# mapping of cite on the sea cost to the code of the sea from spatial data file
GEO_CLAUSE_TO_SEA_CODE = [('CITY_ID IN (35) /*Izmir*/ OR (CITY_ID=48/*Mugla*/ AND COUNTRY_ID IN (1517/*Marmaris*/,1197 /*Bodrum*/))', '28h') # Aegean Sea
                          ,('CITY_ID IN (7 /*Antalya*/,33 /*Mersin*/) OR (CITY_ID=48/*Mugla*/ AND COUNTRY_ID IN (1331/*Fethiye*/, 1742	/*Dalaman*/))','28B') #  Eastern Basin
                    

                    ]
SPATIAL_INTERPOLATION_SICITY_ID=TE_PATH ='/home/dklmn/code/DmitriiK.github.io/RealtyEstimation/' # Path to output folder for spatial interpolation calculati
SAVE_TO_BLOB_STORAGE = False # IF    true, we are saving to data lake as well
