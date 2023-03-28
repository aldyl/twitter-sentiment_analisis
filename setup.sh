#!/bin/bash
sudo apt update
sudo apt upgrade 
sudo apt install mysql-server
sudo service mysql start
pip install -r ./requeriments
