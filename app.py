from flask import Flask
from models.models import db, ws 
#from routes.routes import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    

logging.info("Initializing api...")

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Roberto's CryptoCurrency API!"

if __name__ == '__main__':
    logging.info("Starting api...")
    app.run(host='0.0.0.0', port=5000)