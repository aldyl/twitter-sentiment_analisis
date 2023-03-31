import mysql.connector
from mysql.connector import errorcode, Error, MySQLConnection

DEBUG = True

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
        
        cant_tweet_insertados = 0
        cant_tweet_repetidos = 0

        sql = "INSERT INTO tweets (Id, Date, Content, Impact, Polarity, Objective) VALUES (%s, %s, %s, %s, %s, %s)"
 
        cursor = self.cnx.cursor()

        for tweet in tweets:
            
            if self.tweet_en_bd(tweet[0]) is not None:
                # Inserción de un nuevo tweet
                val = (tweet[0], tweet[1], tweet[2], tweet[3], tweet[4], tweet[5])
                    
                try:
                    cursor.execute(sql, val)
                    # Confirmación de cambios
                    self.cnx.commit()
                    cant_tweet_insertados+=1
                except mysql.connector.Error as err:
                    print(f"Error al crear el registro: {err}")
            else:
                cant_tweet_repetidos+=1

        print(cant_tweet_insertados, " registros insertados.")
        print(cant_tweet_repetidos, " registros repetidos.")
                
      
    def tweet_en_bd(self, tweet_id):
        cursor = self.cnx.cursor()

        # ejecutar la consulta para verificar si el tweet existe
        consulta = f"SELECT * FROM tweets WHERE Id = {tweet_id}"
        
        try:
            cursor.execute(consulta)
            # obtener el resultado de la consulta
            resultado = cursor.fetchone()
        except mysql.connector.Error as err:
                    print(f"Error al ejecutar la consulta: {err}")
        
        if DEBUG: print(consulta)
        # si se encontró el tweet en la base de datos, devolver True
        return resultado
    
    # (Id, Date, Content, Impact, Polarity, Objective) 
    def get_tweet_timelapse_bd(self, columns='*', since='', until=''):
        
        cursor = self.cnx.cursor()

        # ejecutar la consulta para verificar si el tweet existe
        consulta = f"SELECT {columns} FROM tweets WHERE Date >= \"{since}\" and Date <= \"{until}\" "

        try:
            cursor.execute(consulta)
            # obtener el resultado de la consulta
            resultado = cursor.fetchall()

        except mysql.connector.Error as err:
                    print(f"Error al ejecutar la consulta: {err}")

        if DEBUG: print(consulta)

        return resultado

