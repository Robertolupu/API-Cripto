from dotenv import load_dotenv
from pymongo import MongoClient
import os
import logging
import pandas as pd
import json
import websocket
import threading
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    



def on_message(ws, message):

    message = json.loads(message)

    #logging.info(json.loads(message))
    if 'data' in message:

        message['data']['k']['time'] = datetime.now()
        db[message['data']['s']].insert_one(message['data']['k'])


def create_socket(link, coins):

    assets = [coin.lower() + '@kline_1m' for coin in coins]
    assets = '/'.join(assets)
    
    link += 'stream?streams='+assets
    
    ws = websocket.WebSocketApp(link, on_message=on_message)
    
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()

    return ws
    

load_dotenv()


# Database connection

user = os.environ.get('MONGO_ROOT_USER')
password = os.environ.get('MONGO_ROOT_PASSWORD')
MONGO_URI = f'mongodb://{user}:{password}@mongo:27017/?authSource=admin'

client = MongoClient(MONGO_URI)
db = client["CryptoCurrency"]



# Websocket connection

link = user = os.environ.get('WS_LINK')
coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

ws = create_socket(link, coins)