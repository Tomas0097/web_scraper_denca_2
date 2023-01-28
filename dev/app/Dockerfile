# This image must be built from the project root folder. In this case, use
# this script: docker build -t flakooo/myprojects:web_scraper_denca_2-app -f dev/app/Dockerfile .
FROM python:3.12-rc-bullseye
RUN mkdir /opt/web_scraper_denca_2
WORKDIR /opt/web_scraper_denca_2

# Copies and installs requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copies files and sets permissions to be executable.
#COPY dev/app/*.sh /
#RUN chmod +x /*.sh

# Run a file script.
#CMD /docker-start.sh

# Makes a container run without stopping.
ENTRYPOINT ["tail", "-f", "/dev/null"]