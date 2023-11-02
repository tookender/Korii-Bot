FROM python:3.11

WORKDIR /main

COPY . .

RUN apt-get -y update
RUN apt-get install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]