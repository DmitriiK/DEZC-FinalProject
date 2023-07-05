
import psycopg2
# import pandas as pd
from sqlalchemy import create_engine

from metadata import JsonSchema
from settings import SQL_DB, SQL_HOST, SQL_PORT
from creds import SQL_PASSWORD, SQL_USER


class db_worker():

    def __init__(self):
        self.create_connection()
        self.lst_flds = [JsonSchema.flat_name(x) for x in JsonSchema.hepsiemlak_source_fields] + ['is_furnished']  # ((
    
    def __del__(self):
        if self.connection:
            self.curr.close()
            self.connection.close()
    
    def create_connection(self):
        self.connection = psycopg2.connect(
            host=SQL_HOST,
            database=SQL_DB, 
            user=SQL_USER,
            password=SQL_PASSWORD,
            port=SQL_PORT)
        self.curr = self.connection.cursor()

    def init_load_session(self):  
        self.curr.execute('INSERT INTO F_LOADS(dt_start) VALUES (now()) RETURNING load_id')
        data = self.curr.fetchone()
        self.load_id = data[0] 



    def close_session(self,status, is_full, items_processed):
        sql = """UPDATE f_loads SET
                    items_processed = %s,
                    is_full = %s,
                    status = %s,
                    dt_end = now()
                    WHERE load_Id = %s"""
        try:
            self.curr.execute(sql, (items_processed, is_full, status, self.load_id))        
            self.connection.commit()
            # Close communication with the PostgreSQL database
            self.curr.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection is not None:
                self.connection.close()





    def store_db(self, item):
        values = tuple([self.load_id] + [item[key] for key in self.lst_flds])
        # values = (11, 39741352, 11, 8500)
        #try:
        sql = f"CALL pr_merge_emlak_data({', '.join(['%s'] * (1 + len(self.lst_flds)))})"
        self.curr.execute(sql, values)
        # except BaseException as e:
        self.connection.commit()

    def get_geo_data_for_spatial_interpolation(self, citi_id):
        raw_prices = []
        try:
            read_emlak_sql = "SELECT  eml.id, eml.room, eml.is_furnished, eml.price, eml.sqm_netsqm, " \
                            "eml.sqm_price, eml.maplocation_lon, eml.maplocation_lat  " \
                            "FROM public.v_emlak eml " \
                            "WHERE eml.room between 1 and 5" \
                            " and eml.is_furnished=1" \
                            " and CITY_ID=%s"
            cursor = self.curr
            cursor.execute(read_emlak_sql,(citi_id,))
     
            row = cursor.fetchone()
            while row is not None:
                # print(output)               
                apt_id, bedrooms, rent,   lon, lat = (int(row[0]), int(row[1]), row[5], float(row[6]), float(row[7]))
                raw_prices.append((bedrooms, rent, lat, lon))
                row = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            raise

        finally:
            # closing database connection.
            if self.connection:
                cursor.close()
                self.connection.close()
        return raw_prices
    

    def get_geo_data(self, citi_id):
        ret = []
        try:
            connection = self.connection
            read_emlak_geo_sql = "SELECT  eml.id, eml.maplocation_lon, eml.maplocation_lat  " \
                             "FROM public.f_emlak eml " \
                             "WHERE id NOT IN (select ID from public.f_emlak_calc) " \
                             "and CITY_ID=%s"                              
            cursor = connection.cursor()
            cursor.execute(read_emlak_geo_sql, (citi_id,))
            row = cursor.fetchone() 
            while row is not None:
                # print(output)
                id,  lon, lat = (int(row[0]), float(row[1]), float(row[2]))
                ret.append((id, lon, lat))
                row = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching geo data from PostgreSQL", error)
            raise
        return ret

    @staticmethod ##  
    def save_calc_data(df): # pandas geoframe as input
        
        conn_string = f'postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DB}'
        db = create_engine(conn_string)
        conn = db.connect()
        # converting data to sql
        df.to_sql('f_emlak_calc', conn, if_exists= 'append', index = False)
