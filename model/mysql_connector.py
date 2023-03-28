import mysql.connector
from mysql.connector import errorcode


class MysqlConnector:
    def __init__(self):
        self.cnx = 0

        self.TABLA_TWEETS = """
CREATE TABLE tweets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tweet VARCHAR(255) NOT NULL,
  sentiment int(8)
)
"""

    def connect(self, user='root', password='root', host='localhost', database='tweets_bd'):
        # Establecer la conexión a la base de datos
        try:
            self.cnx = mysql.connector.connect(user, password, host, database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cnx.close()

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


