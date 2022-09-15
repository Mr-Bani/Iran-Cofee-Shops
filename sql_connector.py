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
        
    def get_one_table(self,table_name: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM group2.{table_name};",self.cnx)


    
    def get_all_by_filter(self, table_name:str, col_names:list, condition:str = None) -> pd.DataFrame:
        columns_data = {}
        columns_ids = {}

        for i, x in enumerate(col_names):
            name = x
            columns_ids[i] = name
            columns_data[name] = []

        columns = ','.join(col_names)
        command = f"""
            SELECT {columns}
            FROM group2.{table_name}
        """
        if condition != None:
            command += f"WHERE {condition}"
            
        self.cursor.execute(command)

        for x in self.cursor:
            for i, value in enumerate(x):
                name = columns_ids[i]
                columns_data[name] += [value]
        df_filter = pd.DataFrame(data=columns_data)

        return df_filter
    
    def get_all_tables(self) -> pd.DataFrame:
        
        command = """
        SELECT *
            FROM cafe AS c
        INNER JOIN
            cafe_rating AS cr
        ON
            c.cafe_id = cr.cafe_id
        INNER JOIN
            cafe_address AS ca
        ON 
            c.cafe_id = ca.cafe_id
        INNER JOIN
            cafe_features AS cf
        ON
            c.cafe_id = cf.cafe_id
        INNER JOIN
            cafe_location AS cl
        ON
            c.cafe_id = cl.cafe_id            
        """
        self.cursor.execute(command)
        num_fields = len(self.cursor.description)
        field_names = [i[0] for i in self.cursor.description]

        columns_data = {}
        columns_ids = {}

        for i, name in enumerate(field_names):
            columns_ids[i] = name
            columns_data[name] = []

        for x in self.cursor:
            count_id = 0
            count_cost = 0

            for i, value in enumerate(x):
                name = columns_ids[i] 
                if name == 'cafe_id':
                    count_id += 1
                elif name == 'cost':
                    count_cost += 1   

                if name=='cafe_id' and count_id > 1:
                    continue
                elif name=='cost' and count_cost > 1:
                    continue
                else:
                    columns_data[name] += [value]
        df_all_tables = pd.DataFrame(columns_data)

        df_all_tables["work_start"] = df_all_tables["work_start"].values.astype("datetime64")
        df_all_tables["work_end"] = df_all_tables["work_end"].values.astype("datetime64")
        df_all_tables["work_start"] = df_all_tables["work_start"].transform(lambda x: x.strftime("%H:%M"))
        df_all_tables["work_end"] = df_all_tables["work_end"].transform(lambda x: x.strftime("%H:%M"))
        return df_all_tables
    

    def insert(self,cafe : dict):
        #insert cafe to main table
        command = "INSERT INTO group2.cafe (cafe_name, city, province, phone_number, cost, work_start, work_end,type)"
        command+= f" VALUES ('{cafe['cafe_name']}', '{cafe['city']}', '{cafe['province']}',{cafe['phone_number']},{cafe['cost']},'{cafe['work_start']}','{cafe['work_end']}'),{cafe['type']};"

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

        #insert lat and long
        command = "INSERT INTO group2.cafe_location (cafe_id, latitude, longitude)"
        command+= f"VALUES ({cafe_id}, {cafe['lat']}, {cafe['lon']});"
        self.cursor.execute(command)
        self.cnx.commit()


