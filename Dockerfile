FROM python:3

WORKDIR /home/ekaterina/Work/FlaskPrj

COPY . /home/ekaterina/Work/FlaskPrj
  
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "server.py"]

EXPOSE 8000
