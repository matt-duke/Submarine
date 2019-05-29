#!/bin/bash

apt-get install python3-venv
apt-get install libapache2-mod-wsgi-py3 python-dev
apt-get install apache2

rm -r venv
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt

cp /home/pi/Submarine-v2/server/submarine.conf /etc/apache2/sites-available/submarine.conf
systemctl reload apache2