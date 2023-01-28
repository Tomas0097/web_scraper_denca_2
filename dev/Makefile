.DEFAULT_GOAL := default
SHELL := /bin/bash

up:
	sudo docker-compose up -d

down:
	sudo docker-compose down

bash:
	sudo docker exec -it web_scraper_denca_2-app bash

start_app:
	docker exec -it web_scraper_denca_2-app bash -c 'python3 src/main.py'