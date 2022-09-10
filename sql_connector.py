import mysql.connector
import pandas as pd
class sql_connector:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = None
        self.cnx = None
        self.port = port
        self.connect()

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database,port=self.port)
        self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()
        
    def get_all_table(self,table_name: str) -> pd.DataFrame:

        self.cursor.execute(f"DESCRIBE {table_name}")
        columns_data = {}
        columns_ids = {}

        for i, x in enumerate(self.cursor):
            name = x[0]
            columns_ids[i] = name
            columns_data[name] = []

        command = f"SELECT * FROM {table_name}"
        self.cursor.execute(command)

        for x in self.cursor:
            for i, value in enumerate(x):
                name = columns_ids[i]
                columns_data[name] += [value]
        df = pd.DataFrame(data=columns_data)

        return df

    def insert(self,cafe : dict):
        #insert cafe to main table
        command = "INSERT INTO group2.cafe (cafe_name, city, province, phone_number, cost, work_start, work_end)"
        command+= f" VALUES ('{cafe['cafe_name']}', '{cafe['city']}', '{cafe['province']}',{cafe['phone_number']},{cafe['cost']},'{cafe['work_start']}','{cafe['work_end']}');"

        self.cursor.execute(command)
        self.cnx.commit()

        #get cafe_id from table
        command = "SELECT cafe_id FROM group2.cafe ORDER BY cafe_id DESC LIMIT 1;"
        self.cursor.execute(command)
        cafe_id = self.cursor.fetchall()[0][0]

        #insert cafe_address
        command = "INSERT INTO group2.cafe_address (cafe_id, cafe_address)"
        command+= f"VALUES ({cafe_id}, '{cafe['cafe_address']}');"

        self.cursor.execute(command)
        self.cnx.commit()

        #insert cafe_rating
        command = "INSERT INTO group2.cafe_rating (cafe_id, food_quality, service_quality, cost,cost_value, environment)"
        command+= f"VALUES ({cafe_id}, {cafe['food_quality']}, {cafe['service_quality']},{cafe['cost']},{cafe['cost_value']},{cafe['environment']});"
        self.cursor.execute(command)
        self.cnx.commit()

        #insert cafe_features
        command = "INSERT INTO group2.cafe_features (cafe_id, hookah,internet, delivery, smoking, open_space, live_music, parking, pos)"
        command+= f"VALUES ({cafe_id}, {cafe['hookah']}, {cafe['internet']},{cafe['delivery']},{cafe['smoking']},{cafe['open_space']}, {cafe['live_music']}, {cafe['parking']},{cafe['pos']});"
        self.cursor.execute(command)
        self.cnx.commit()















