#!/bin/bash
sudo apt update
sudo apt upgrade 
sudo apt install mysql-server
sudo service mysql restart
sudo -H pip3 install pipenv
pipenv install --skip-lock  -r ./requeriments
python3 -m nltk.downloader all
