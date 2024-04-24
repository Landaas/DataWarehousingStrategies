FROM python:3.8-slim

WORKDIR /data

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./init_dw.py"]
