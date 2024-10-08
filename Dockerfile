FROM python:3.11

WORKDIR /main

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip list
    
COPY . .

EXPOSE 6969

CMD ["python", "main.py"]