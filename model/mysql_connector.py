import mysql.connector
from mysql.connector import errorcode, Error, MySQLConnection

DEBUG = False

class MysqlConnector:
    def __init__(self, user, password,
                 host, database):

        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def connect(self):
        # Establecer la conexión a la base de datos
        try:

            cnx = mysql.connector.connect(user=self.user, password=self.password,
                                          host=self.host, database=self.database,
                                          auth_plugin='mysql_native_password')

            if DEBUG:
                db_Info = cnx.get_server_info()
                print("Connected to MySQL Server version ", db_Info)

                cursor = cnx.cursor()
                cursor.execute("select database();")

                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                print("Review Mysql server status")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Other", err)

        return cnx

    def create_tweet_table(self, table):

        self.TABLA_TWEETS = f"""
CREATE TABLE {table} (
  Id NUMERIC(30) UNSIGNED NOT NULL,
  Date DATE NOT NULL,
  Content TEXT NOT NULL,
  Impact FLOAT NOT NULL,
  Polarity FLOAT NOT NULL,
  Objective FLOAT NOT NULL,
  PRIMARY KEY (Id)
);
"""
        cnx = self.connect()

        try:

            cursor = cnx.cursor()

            if self.table_on_db(table):

                if DEBUG: print("Table {table}, are present")

            else:
                cursor.execute(self.TABLA_TWEETS)
                if DEBUG: print("Table {table}, build ok")

        except mysql.connector.Error as err:

            print(f"Look this error for table {table} : \n {err}")

        finally:

            cnx.close()

    def insert_tweet_on_table(self, table, tweets):

        cant_tweet_inserted = 0
        cant_tweet_repeated = 0

        sql = f"INSERT INTO {table} (Id, Date, Content, Impact, Polarity, Objective) VALUES (%s, %s, %s, %s, %s, %s)"

        cnx = self.connect()

        try:

            for tweet in tweets:

                try:
                    if self.id_on_table_bd(table, id=tweet[0]) is None:
                        # Insert new tweet
                        val = (tweet[0], tweet[1], tweet[2],
                               tweet[3], tweet[4], tweet[5])

                        cursor = cnx.cursor()

                        cursor.execute(sql, val)

                        cnx.commit()

                        cant_tweet_inserted += 1

                    else:

                        cant_tweet_repeated += 1

                except mysql.connector.Error as err:

                    print(f"Error al crear el registro: {err}")

                finally:
                    cursor.close()

        finally:
            cnx.close()

        if DEBUG:

            print("Inser into SQL db")
            print(cant_tweet_inserted, " registros insertados.")
            print(cant_tweet_repeated, " registros repetidos.")

    def table_on_db(self, table):

        cnx = self.connect()

        try:

            cursor = cnx.cursor()

            cursor.execute(f"SHOW TABLES LIKE '{table}';")

            if  cursor.fetchone() is None:
                if DEBUG: print(f"False {table}")
                cnx.close()
                return False
            else:
                if DEBUG: print(f"True {table}")
                cnx.close()
                return True

        except mysql.connector.Error as err:

            print(f"Look this error for table {table} : \n {err}")

        finally:
            cnx.close()

    def id_on_table_bd(self, table, id):

        consult = f"SELECT * FROM {table} WHERE Id = {id}"
        
        if DEBUG: print(consult)

        if self.table_on_db(table):

            cnx = self.connect()

            try:

                cursor = cnx.cursor()

                cursor.execute(consult)

                out = cursor.fetchone()

            except mysql.connector.Error as err:

                print(f"Look this error: \n {err}")

            finally:
                cursor.close()
                cnx.close()
                return out


    def get_timelapse_bd(self, table='', columns='*', since='', until='') -> list:

        consult = f"SELECT {columns} FROM {table} WHERE Date >= \"{since}\" and Date <= \"{until}\" "

        cnx = self.connect()

        try:

            cursor = cnx.cursor()
            cursor.execute(consult)
            result = cursor.fetchall()
            cursor.close()

        except mysql.connector.Error as err:

            print(f"Look this error: \n {err}")

        finally:
            cnx.close()

        if DEBUG:
            print(result)

        return result
