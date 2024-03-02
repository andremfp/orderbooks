import time
import sqlite3
import pandas as pd

db = 'orderbook.db'

def initDatabase():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for orderbook
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orderbook (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            exchange TEXT,
            symbol TEXT,
            type TEXT,
            price REAL,
            quantity REAL
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

    cursor.execute('DELETE FROM orderbook')

    for bid in data['bids']:
        cursor.execute('''
            INSERT INTO orderbook (timestamp, exchange, symbol, type, price, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, exchange, symbol, 'bid',float(bid[0]), float(bid[1])))

    for ask in data['asks']:
        cursor.execute('''
            INSERT INTO orderbook (timestamp, exchange, symbol, type, price, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, exchange, symbol, 'ask', float(ask[0]), float(ask[1])))

    conn.commit()
    conn.close()

def storeStats(data, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO stats (timestamp, exchange, symbol, totalBidVolume, totalAskVolume)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, exchange, symbol,float(data[0]), float(data[1])))

    conn.commit()
    conn.close()

def getQuantities():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f'SELECT quantity FROM orderbook WHERE type="bid"')
    bidQuantities = [row[0] for row in cursor.fetchall()]

    cursor.execute(f'SELECT quantity FROM orderbook WHERE type="ask"')
    askQuantities = [row[0] for row in cursor.fetchall()]

    conn.close()
    return bidQuantities, askQuantities

# Function to fetch data from SQLite database
def getDataToResample():
    conn = sqlite3.connect(db)
    
    data = pd.read_sql_query(f'SELECT price, quantity, type FROM orderbook ORDER BY price', conn)
    
    conn.close()
    return data
