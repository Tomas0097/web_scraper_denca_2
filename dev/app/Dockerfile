FROM python:3.12-rc-bullseye
RUN mkdir -p /opt/web_scraper_denca_2
WORKDIR /opt/web_scraper_denca_2

# install requirements.txt
COPY requirements.txt .
RUN pip3 install -U pip
RUN pip3 install --no-cache-dir --force-reinstall -r requirements.txt