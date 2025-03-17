FROM python:3.11-slim

WORKDIR /main

RUN apt-get update && apt-get upgrade -y && apt-get install -y neofetch

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6969

CMD ["python", "main.py"]
