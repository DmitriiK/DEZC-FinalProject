
import psycopg2
from metadata import JsonSchema
from settings import SQL_DB, SQL_HOST
from creds import SQL_PASSWORD, SQL_USER


class db_worker():

    def __init__(self):
        self.create_connection()
        self.lst_flds = [JsonSchema.flat_name(x) for x in JsonSchema.hepsiemlak_source_fields] + ['is_furnished']  # ((
    
    def __del__(self):
        if self.connection:
            self.curr.close()
            self.connection.close()

    def init_load_session(self):  
        self.curr.execute('INSERT INTO F_LOADS(dt_start) VALUES (now()) RETURNING load_id')
        data = self.curr.fetchone()
        self.load_id = data[0]    


    def create_connection(self):
        self.connection = psycopg2.connect(
            host=SQL_HOST,
            database=SQL_DB, 
            user=SQL_USER,
            password=SQL_PASSWORD)

        self.curr = self.connection.cursor()


    def store_db(self, item):
        values = tuple([self.load_id] + [item[key] for key in self.lst_flds])
        # values = (11, 39741352, 11, 8500)
        #try:
        sql = f"CALL pr_merge_emlak_data({', '.join(['%s'] * (1 + len(self.lst_flds)))})"
        self.curr.execute(sql, values)
        # except BaseException as e:
        self.connection.commit()

    def get_geo_data(self):
        ret = []
        try:
            connection = self.connection
            read_emlak_geo_sql = "SELECT  eml.id, eml.maplocation_lon, eml.maplocation_lat  " \
                             "FROM public.f_emlak eml " \
                             "WHERE load_id IN (select max(load_id) from public.f_emlak) " 
            cursor = connection.cursor()
            cursor.execute(read_emlak_geo_sql)
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