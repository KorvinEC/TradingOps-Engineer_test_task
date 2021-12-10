FROM python:3.8.2
ADD main.py .
ADD BinanceManager.py .
ADD WebsocketConnection.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
