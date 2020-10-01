FROM python:3.7.7

# To enable logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create server directory
RUN mkdir /srv/project
WORKDIR /srv/project

# Install the server dependencies
COPY requirements.txt /srv/project
RUN pip install -r requirements.txt

# Bundle the source
COPY . /srv/project