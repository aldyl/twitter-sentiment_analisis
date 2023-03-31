#!/bin/bash
sudo apt update
sudo apt upgrade

# Install mysql server
sudo apt install mysql-server
sudo systemctl start mysql.service
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';"
echo "Use password as pass"
sudo mysql_secure_installation
sudo mysql -u root -p -e  "CREATE USER 'twitter'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';"
sudo mysql -u root -p -e  "GRANT CREATE, ALTER, DROP, INSERT, UPDATE, INDEX, DELETE, SELECT, REFERENCES, RELOAD on *.* TO ' twitter '@'localhost' WITH GRANT OPTION;"
sudo mysql -u root -p -e "Create database tweets_bd;"

sudo -H pip3 install pipenv
pipenv install --skip-lock  -r ./requeriments
python3 -m nltk.downloader all
