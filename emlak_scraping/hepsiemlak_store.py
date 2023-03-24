
import psycopg2
from metadata import JsonSchema
from settings import SQL_DB, SQL_HOST
from creds import SQL_PASSWORD, SQL_USER


class save_to_db():

    def __init__(self):
        self.create_connection()
        self.curr.execute('INSERT INTO F_LOADS(dt_start) VALUES (now()) RETURNING load_id')
        data = self.curr.fetchone()
        self.load_id = data[0]
        self.lst_flds = [JsonSchema.flat_name(x) for x in JsonSchema.hepsiemlak_source_fields] + ['is_furnished']  # ((

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
