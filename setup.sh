#!/bin/bash
sudo apt update
sudo apt upgrade 
sudo apt install mysql-server
sudo service mysql start
pip3 install pipenv
pipenv install --skip-lock  -r ./requeriments