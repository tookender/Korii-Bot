FROM python:3.11

WORKDIR /main

COPY . .

RUN apt-get -y update
RUN apt-get install -y ffmpeg

RUN pip install -r requirements.txt

EXPOSE 6969

CMD ["python", "main.py"]