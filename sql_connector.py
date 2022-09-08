import mysql.connector

class sql_connector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = None
        self.cnx = None
        self.connect()

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
        self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def insert(self,cafe : dict) -> "Inserts a coffee into the database":
        command = "INSERT INTO table_name (cafe_name, city, province, phone_number, cost, work_start, work_end)"
        command+= f"VALUES ({cafe['cafe_name']}, {cafe['city']}, {cafe['province']},{cafe['phone_nummber']},{cafe['cost']},{cafe['work_start']},{cafe['work_end']});"
        self.cursor.execute(command)
        self.cnx.commit()







