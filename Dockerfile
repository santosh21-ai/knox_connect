FROM python:3.11.4-slim-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /knox

# Set the working directory to /knox
WORKDIR /knox

# Copy the current directory contents into the container at /knox
ADD . /knox/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# RUN apt-get update && apt-get install -y libsqlite3-dev
# RUN pip install --upgrade sqlite3