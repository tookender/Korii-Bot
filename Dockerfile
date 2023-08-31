FROM python:bullseye

WORKDIR /main

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]

EXPOSE 5432