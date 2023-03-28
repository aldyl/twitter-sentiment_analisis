#!/bin/python3

import mysql.connector
from mysql.connector import errorcode



class MysqlConnector:
    def __init__(self):
        self.cnx = 0
        self.tabla_tweets = """
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
            cnx.close()

    # Crear la tabla para los tweets
cursor = cnx.cursor()

tabla_tweets = """
CREATE TABLE tweets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tweet VARCHAR(255) NOT NULL
)
"""

try:
    cursor.execute(tabla_tweets)
except mysql.connector.Error as err:
    print(f"Error al crear la tabla: {err}")
else:
    print("Tabla creada correctamente")

# Recorrer los tweets y guardarlos en la base de datos
for tweet in tweets:
    agregar_tweet = """
    INSERT INTO tweets (tweet) VALUES (%s)
    """
    cursor.execute(agregar_tweet, (tweet,))

# Confirmar los cambios y cerrar la conexión
cnx.commit()
cursor.close()
cnx.close()
