FROM python:latest
WORKDIR /main
COPY . .
RUN pip install -r requirements.txt
RUN apt install neofetch
CMD ["python", "bot.py"]
