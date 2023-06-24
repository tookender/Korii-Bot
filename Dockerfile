FROM python:latest
WORKDIR /main
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
