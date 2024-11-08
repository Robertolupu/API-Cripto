FROM python:3.13

RUN pip install flask pymongo python-dotenv pandas websocket-client matplotlib PyJWT

WORKDIR /app
COPY . .

CMD ["python", "app.py"]