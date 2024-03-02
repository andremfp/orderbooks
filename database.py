import json
import sqlite3
import pandas as pd
import ast

db = 'orderbook.db'

def initDatabase():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for orderbook
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

def storeOrderbook(data, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO orderbook (timestamp, exchange, symbol, bids, asks)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, exchange, symbol, json.dumps(data['bids']), json.dumps(data['asks'])))

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

def getBidsAsksLists(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f'SELECT bids, asks FROM orderbook WHERE exchange="{exchange}" AND symbol="{symbol}"')
    data = cursor.fetchall()[0]
    bids = ast.literal_eval(data[0])
    asks = ast.literal_eval(data[1])

    conn.close()
    return bids, asks
