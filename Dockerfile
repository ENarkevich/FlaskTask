#FROM ubuntu:18.04
FROM python:3

WORKDIR /home/ekaterina/Work/FlaskPrj

COPY . /home/ekaterina/Work/FlaskPrj

#RUN apt-get update \
#    && apt-get install -y python3-pip python3-dev 
  
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "server.py"]

EXPOSE 8000
