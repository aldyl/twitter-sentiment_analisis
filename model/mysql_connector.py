import mysql.connector
from mysql.connector import errorcode, Error, MySQLConnection

DEBUG = False


class MysqlConnector:
    def __init__(self, user, password,
                 host, database):
        self.cnx = MySQLConnection()

        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def connect(self):
        # Establecer la conexión a la base de datos
        try:
            self.cnx = mysql.connector.connect(user=self.user, password=self.password,
                                               host=self.host, database=self.database,
                                               auth_plugin='mysql_native_password')

            db_Info = self.cnx.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = self.cnx.cursor()
            cursor.execute("select database();")

            record = cursor.fetchone()
            print("You're connected to database: ", record)

        except Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Other", err)

    def close(self):
        if self.cnx.is_connected():
            self.cnx.close()

            print("MySQL connection is closed")

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
        try:
            self.cnx.connect()
            cursor = self.cnx.cursor()
            if cursor.execute(f"SHOW TABLES LIKE '{table}';") is None:
                cursor.execute(self.TABLA_TWEETS)
                print("Table {table}, build ok")
            else:
                print("Table {table}, are present")

        except mysql.connector.Error as err:

            print(f"Look this error for table {table} : \n {err}")

        finally:
            self.cnx.close()


    def insert_tweet_on_table(self, table, tweets):

        cant_tweet_inserted = 0
        cant_tweet_repeated = 0

        sql = f"INSERT INTO {table} (Id, Date, Content, Impact, Polarity, Objective) VALUES (%s, %s, %s, %s, %s, %s)"

        cursor = self.cnx.cursor()

        try:
            
            self.cnx.connect()

            for tweet in tweets:

                try:
                    if self.tweet_en_bd(table, tweet_id=tweet[0]) is None:
                        # Insert new tweet
                        val = (tweet[0], tweet[1], tweet[2], tweet[3], tweet[4], tweet[5])

                        cursor = self.cnx.cursor()

                        cursor.execute(sql, val)

                        self.cnx.commit()

                        cant_tweet_inserted += 1

                    else:

                        cant_tweet_repeated += 1

                except mysql.connector.Error as err:

                        print(f"Error al crear el registro: {err}")
                
                finally:
                        cursor.close()
                  
        finally:
            self.cnx.close()


        if DEBUG:
            print("Inser into SQL db")
            print(cant_tweet_inserted, " registros insertados.")
            print(cant_tweet_repeated, " registros repetidos.")

    def tweet_en_bd(self, table, tweet_id):

        consult = f"SELECT * FROM {table} WHERE Id = {tweet_id}"

        try:
            self.cnx.connect()

            cursor = self.cnx.cursor()

            cursor.execute(consult)
            result = cursor.fetchone()
            cursor.close()

        except mysql.connector.Error as err:

            print(f"Look this error: \n {err}")

        finally:
            self.cnx.close()
        
        if DEBUG:
            print(result)

        return result

    # (Id, Date, Content, Impact, Polarity, Objective)
    def get_tweet_timelapse_bd(self, table, columns='*', since='', until='') -> list:

        consult = f"SELECT {columns} FROM {table} WHERE Date >= \"{since}\" and Date <= \"{until}\" "

        try:
            self.cnx.connect()

            cursor = self.cnx.cursor()

            cursor.execute(consult)
            result = cursor.fetchall()
            cursor.close()

        except mysql.connector.Error as err:

            print(f"Look this error: \n {err}")

        finally:
            self.cnx.close()
        
        if DEBUG:
            print(result)

        return result
