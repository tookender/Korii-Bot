FROM python:3.11-slim

WORKDIR /main

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
    
COPY . .

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y neofetch

EXPOSE 6969

CMD ["python", "main.py"]