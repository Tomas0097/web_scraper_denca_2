#!/bin/bash

cd /opt/web_scraper_denca_2

# install/upgrade Python packages based on requirements.txt
pip3 install --no-cache-dir -r requirements.txt

python3 src/main.py