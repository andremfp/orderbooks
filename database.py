import json
import sqlite3
import ast

db = 'orderbook.db'

def initDatabase():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for orderbooks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orderbook (
            timestamp DATETIME,
            exchange TEXT,
            symbol TEXT,
            bids TEXT,
            asks TEXT,
            PRIMARY KEY (exchange, symbol)
        )
    ''')

    # Table for stats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            exchange TEXT,
            symbol TEXT,
            totalBidVolume FLOAT,
            totalAskVolume FLOAT
        )
    ''')

    # Table for resampled orderbooks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resampledOrderbooks (
            timestamp DATETIME,
            exchange TEXT,
            symbol TEXT,
            binnedOrderbook TEXT,
            PRIMARY KEY (exchange, symbol)
        )
    ''')

def storeOrderbook(data, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Convert bids and asks to float
    bids = [[float(elem) for elem in bid] for bid in data['bids']]
    asks = [[float(elem) for elem in ask] for ask in data['asks']]

    cursor.execute('''
        INSERT OR REPLACE INTO orderbook (timestamp, exchange, symbol, bids, asks)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, exchange, symbol, json.dumps(bids), json.dumps(asks)))

    conn.commit()
    conn.close()

def storeStats(totalBidVolume, totalAskVolume, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO stats (timestamp, exchange, symbol, totalBidVolume, totalAskVolume)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, exchange, symbol, totalBidVolume, totalAskVolume))

    conn.commit()
    conn.close()

def storeResampledOrderbook(data, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO resampledOrderbooks (timestamp, exchange, symbol, binnedOrderbook)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, exchange, symbol, json.dumps(data)))

    conn.commit()
    conn.close()

def getBidsAsksLists(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f'SELECT bids, asks FROM orderbook WHERE exchange="{exchange}" AND symbol="{symbol}"')
    data = cursor.fetchall()[0]
    bids = ast.literal_eval(data[0])
    asks = ast.literal_eval(data[1])

    bids = [[float(elem) for elem in bid] for bid in bids]
    asks = [[float(elem) for elem in ask] for ask in asks]

    conn.close()
    return bids, asks