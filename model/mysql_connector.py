import mysql.connector
from mysql.connector import errorcode, Error


class MysqlConnector:
    def __init__(self):
        
        self.cnx = any

        self.TABLA_TWEETS = """
CREATE TABLE tweets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tweet VARCHAR(255) NOT NULL,
  sentiment int(8)
)
"""

    def connect(self, user_I='root', password_I='root', host_I='localhost', database_I='tweets_bd'):
        # Establecer la conexión a la base de datos
        try:
            self.cnx = mysql.connector.connect(user=user_I, password=password_I, host=host_I, database=database_I)

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
                print(err)

    def close(self):
        if self.cnx.is_connected():
            self.cnx.close()
            print("MySQL connection is closed")

    def create_tweet_table(self):

        cursor = self.cnx.cursor()
        
        try:
            cursor.execute(self.TABLA_TWEETS)
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")
        else:
            print("Tabla creada correctamente")


    def insert_tweet_on_table(self, tweets):

        cursor = self.get_cursor()

        for tweet in tweets:
            
            agregar_tweet = """
INSERT INTO tweets (tweet) VALUES (%s)
"""
        cursor.execute(agregar_tweet, (tweet,))
        
        self.cnx.commit()
        cursor.close()
        self.cnx.close()


    def get_tweets_from_table(self):
        
        cursor = self.cnx.cursor()
       
        query = "SELECT tweet,sentiment FROM tweets"
        
        cursor.execute(query)

        tweets = cursor.fetchall()

        cursor.close()

        self.cnx.close()

        return tweets


