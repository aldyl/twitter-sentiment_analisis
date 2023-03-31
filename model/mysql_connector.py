import mysql.connector
from mysql.connector import errorcode, Error, MySQLConnection


class MysqlConnector:
    def __init__(self):
        self.cnx = MySQLConnection()

    def connect(self, user_I='twitter', password_I='password', host_I='localhost', database_I='tweets_bd'):
        # Establecer la conexión a la base de datos
        try:
            self.cnx = mysql.connector.connect(user=user_I, password=password_I,
                                                host=host_I, database=database_I,
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
                print("Other",err)

    def close(self):
        if self.cnx.is_connected():
            self.cnx.close()
            print("MySQL connection is closed")

    def create_tweet_table(self):

        self.TABLA_TWEETS = """
CREATE TABLE tweets (
  Id NUMERIC(30) UNSIGNED NOT NULL,
  Date DATE NOT NULL,
  Content TEXT NOT NULL,
  Impact FLOAT NOT NULL,
  Polarity FLOAT NOT NULL,
  Objective FLOAT NOT NULL,
  PRIMARY KEY (Id)
);
"""

        cursor = self.cnx.cursor()
        
        try:
            cursor.execute(self.TABLA_TWEETS)
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")
        else:
            print("Tabla creada correctamente")


    def insert_tweet_on_table(self, tweets):

        cursor = self.cnx.cursor()


        for tweet in tweets:
            
            if not self.tweet_en_bd(tweet[0]):
                # Inserción de un nuevo tweet
                sql = "INSERT INTO tweets (Id, Date, Content, Impact, Polarity, Objective) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (int(tweet[0]), tweet[1], tweet[2], tweet[3], tweet[4], tweet[5])
            
                try:
                    cursor.execute(sql, val)
                    # Confirmación de cambios
                    self.cnx.commit()
                except mysql.connector.Error as err:
                    print(f"Error al crear el registro: {err}")

        print(cursor.rowcount, "registros insertados.")
                
      

    def tweet_en_bd(self, tweet_id):
        cursor = self.cnx.cursor()

        # ejecutar la consulta para verificar si el tweet existe
        consulta = f"SELECT * FROM tweets WHERE Id = {tweet_id}"
        cursor.execute(consulta)
        # obtener el resultado de la consulta
        resultado = cursor.fetchone()

        # si se encontró el tweet en la base de datos, devolver True
        if resultado is not None:
            return True
        else:
            return False
    
    
    def get_tweets_from_table_id(self, id):
        
        cursor = self.cnx.cursor()
       
        query = "SELECT * FROM tweets WHERE %s == tweets.Id"
        
        cursor.execute(query)

        tweets = cursor.fetchall()

        cursor.close()

        self.cnx.close()

        return tweets


