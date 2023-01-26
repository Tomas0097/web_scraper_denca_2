FROM python:3.12-rc-bullseye
RUN mkdir /opt/web_scraper_denca_2
WORKDIR /opt/web_scraper_denca_2

# Copies and installs requirements.txt -> This image must be built from the project
# root folder. In this case, it is 'web_scraper_denca_2.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copies files and allows them to be executable.
#COPY dev/app/*.sh /
#RUN chmod +x /*.sh

# Run a file script.
#CMD /docker-start.sh

# Makes a container run without stopping.
ENTRYPOINT ["tail", "-f", "/dev/null"]