import mysql.connector
from mysql.connector import Error

DEBUG = True


class MysqlConnector():

    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.cnx = None

    def connect(self):
        if not self.cnx:
            try:
                self.cnx = mysql.connector.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    database=self.database,
                    auth_plugin='mysql_native_password'
                )

                if DEBUG:
                    db_Info = self.cnx.get_server_info()
                    print("Connected to MySQL Server version ", db_Info)

                    cursor = self.cnx.cursor()
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    print("You're connected to database: ", record)
                    cursor.close()

            except Error as err:
                print(f"Error connecting to database '{self.database}': {err}")

        return self.cnx

    def create_tweet_table(self, table):
        tabla_tweets = """
            CREATE TABLE IF NOT EXISTS %s (
                Id NUMERIC(30) UNSIGNED NOT NULL,
                Date DATE NOT NULL,
                Content TEXT NOT NULL,
                Impact FLOAT NOT NULL,
                Polarity FLOAT NOT NULL,
                Objective FLOAT NOT NULL,
                PRIMARY KEY (Id)
            );
        """

        try:
            cursor = self.cnx.cursor()
            cursor.execute(tabla_tweets % (table))
            if DEBUG:
                print(f"Table {table} created successfully")
            self.cnx.commit()
        except mysql.connector.Error as err:
            if self.cnx and self.cnx.is_connected():
                if self.cnx.in_transaction:
                    self.cnx.rollback()
                print(f"Error creating table '{table}': {err}")

    def table_on_db(self, table):
       
        try:
            cursor = self.cnx.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", (table,))
            count = cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            print(f"Error checking table {table}: {err}")

    def insert_tweet_batch_on_table(self, table, tweets):

        cant_tweet_inserted = 0
        cant_tweet_repeated = 0

        sql = "INSERT INTO {} (Id, Date, Content, Impact, Polarity, Objective) VALUES (%s, %s, %s, %s, %s, %s)".format(
            table)
      
        for tweet in tweets:
            try:
                if self.id_on_table_bd(table, id=tweet[0]) is None:
                    # Insert new tweet
                    val = (tweet[0], tweet[1], tweet[2],
                           tweet[3], tweet[4], tweet[5])
                         
                    cursor = self.cnx.cursor()
                    cursor.execute(sql, val)
                    self.cnx.commit()
                    cant_tweet_inserted += 1
                else:
                    cant_tweet_repeated += 1
            except mysql.connector.Error as err:
                if self.cnx and self.cnx.is_connected():
                    if self.cnx.in_transaction:
                        self.cnx.rollback()
                print(f"Error al crear el registro: {err}")
        if DEBUG:
            print("Insert into SQL db")
            print(cant_tweet_inserted, " registros insertados.")
            print(cant_tweet_repeated, " registros repetidos.")

    def id_on_table_bd(self, table, id):

        consult = "SELECT * FROM {} WHERE Id = %s".format(table)

        try:

            cursor = self.cnx.cursor()
            cursor.execute(consult, (id,))
            out = cursor.fetchone()
            return out
        except mysql.connector.Error as err:
            print(f"Error checking id {id} on {table}: {err}")

    def get_timelapse_bd(self, table, columns='*', since='', until='') -> list:
        if not table:
            raise ValueError("The 'table' parameter cannot be empty")

        consult = "SELECT {} FROM {} WHERE Date >= %s and Date <= %s".format(
            columns, table)
        data = (since, until)

        try:
            cursor = self.cnx.cursor()
            cursor.execute(consult, data)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Look this error: \n {}".format(err))