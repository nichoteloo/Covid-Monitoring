#Create a ubuntu base image with python 3 installed.
FROM python:3.8

#Set the working directory
WORKDIR /app

#copy all the files
COPY . /app

#Install the dependencies
RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

# #Expose the required port
# EXPOSE 5000

#Run the command
CMD gunicorn main:app