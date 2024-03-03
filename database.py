import json
import sqlite3
import ast

db = 'orderbooks.db'

def initDatabase():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for orderbooks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orderbooks (
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

    cursor.execute('''INSERT OR REPLACE INTO orderbooks
                    (timestamp, exchange, symbol, bids, asks)
                    VALUES (?, ?, ?, ?, ?)''', (timestamp, exchange, symbol, json.dumps(bids), json.dumps(asks)))

    conn.commit()
    conn.close()

def storeStats(totalBidVolume, totalAskVolume, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO stats
                    (timestamp, exchange, symbol, totalBidVolume, totalAskVolume)
                    VALUES (?, ?, ?, ?, ?)''', (timestamp, exchange, symbol, totalBidVolume, totalAskVolume))

    conn.commit()
    conn.close()

def storeResampledOrderbook(data, exchange, symbol, timestamp):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''INSERT OR REPLACE INTO resampledOrderbooks 
                    (timestamp, exchange, symbol, binnedOrderbook)
                    VALUES (?, ?, ?, ?)''', (timestamp, exchange, symbol, json.dumps(data)))

    conn.commit()
    conn.close()

def getBidsAsksLists(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT bids, asks
                    FROM orderbooks
                    WHERE exchange = ? AND symbol = ?''', (exchange, symbol))

    data = cursor.fetchall()[0]
    bids = ast.literal_eval(data[0])
    asks = ast.literal_eval(data[1])

    bids = [[float(elem) for elem in bid] for bid in bids]
    asks = [[float(elem) for elem in ask] for ask in asks]

    conn.close()
    return bids, asks

def getOrderbook(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, bids, asks
                    FROM orderbooks
                    WHERE exchange = ? AND symbol = ?''', (exchange, symbol))

    return cursor.fetchone()

def getResampledOrderbook(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, binnedOrderbook
                    FROM resampledOrderbooks
                    WHERE exchange = ? AND symbol = ?''', (exchange, symbol))

    return cursor.fetchone()

def getStats(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, totalBidVolume, totalAskVolume
                    FROM stats
                    WHERE exchange = ? AND symbol = ?
                    AND timestamp = (
                        SELECT MIN(timestamp)
                        FROM stats
                        WHERE exchange = ? AND symbol = ?
                    )
                    ''', (exchange, symbol, exchange, symbol))

    return cursor.fetchone()

def getAllStats(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, totalBidVolume, totalAskVolume
                    FROM stats
                    WHERE exchange = ? AND symbol = ?
                    ORDER BY timestamp
                    ''', (exchange, symbol))

    return cursor.fetchall()