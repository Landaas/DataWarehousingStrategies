FROM python:3.8-slim

WORKDIR /data

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc  

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./init_dw.py"]
