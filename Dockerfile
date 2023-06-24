FROM python:latest
WORKDIR /main
COPY . .
RUN pip install -r requirements.txt
RUN apt update && apt install -y neofetch
CMD ["python", "bot.py"]
