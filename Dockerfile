FROM ubuntu:18.04

WORKDIR /home/ekaterina/Work/FlaskPrj

COPY . /home/ekaterina/Work/FlaskPrj

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev 
   # && pip3 install --upgrade pip \
   # && apt-get install libgtk2.0-dev \
   # && apt-get install -y libsm6 libxext6 libxrender-dev

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "server.py"]

EXPOSE 8000
