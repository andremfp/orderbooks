import json
import sqlite3
import ast
import logging

db = 'orderbooks.db'

# Create db and tables if they don't exist
def initDatabase():
    logging.info('Initializing database...')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for orderbooks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orderbooks (
            timestamp DATETIME,
            exchange TEXT,
            symbol TEXT,
            lastUpdateId INTEGER,
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
    logging.info('Database initialized...')

# Store an orderbook snapshot to the db
def storeOrderbook(data, exchange, symbol, timestamp):
    logging.info('Storing snapshot...')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Convert bids and asks to float
    bids = [[float(elem) for elem in bid] for bid in data['bids']]
    asks = [[float(elem) for elem in ask] for ask in data['asks']]

    cursor.execute('''INSERT OR REPLACE INTO orderbooks
                    (timestamp, exchange, symbol, lastUpdateId, bids, asks)
                    VALUES (?, ?, ?, ?, ?, ?)''', (timestamp, exchange, symbol, data['lastUpdateId'], json.dumps(bids), json.dumps(asks)))

    conn.commit()
    conn.close()
    logging.info('Snapshot stored...')

# Store stats to the db
def storeStats(totalBidVolume, totalAskVolume, exchange, symbol, timestamp):
    logging.info('Storing stats...')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO stats
                    (timestamp, exchange, symbol, totalBidVolume, totalAskVolume)
                    VALUES (?, ?, ?, ?, ?)''', (timestamp, exchange, symbol, totalBidVolume, totalAskVolume))

    conn.commit()
    conn.close()
    logging.info('Stats stored...')

# Store a resampled orderbook to the db
def storeResampledOrderbook(data, exchange, symbol, timestamp):
    logging.info('Storing resampled orderbook...')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''INSERT OR REPLACE INTO resampledOrderbooks 
                    (timestamp, exchange, symbol, binnedOrderbook)
                    VALUES (?, ?, ?, ?)''', (timestamp, exchange, symbol, json.dumps(data)))

    conn.commit()
    conn.close()
    logging.info('Resampled orderbook stored...')

def storeUpdatedOrderbook(lastUpdateId, bids, asks, timestamp, exchange, symbol):
    logging.info('Storing updates...')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''UPDATE orderbooks
                    SET timestamp = ?, lastUpdateId = ?, bids = ?, asks = ?
                    WHERE exchange = ? AND symbol = ?''', (timestamp, lastUpdateId, json.dumps(bids), json.dumps(asks), exchange, symbol))

    conn.commit()
    conn.close()
    logging.info('Updates stored...')

# Fetch bids and asks from an orderbook. Return them as lists
def getBidsAsksLists(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT lastUpdateId, bids, asks
                    FROM orderbooks
                    WHERE exchange = ? AND symbol = ?''', (exchange, symbol))

    data = cursor.fetchall()[0]
    lastUpdateId = data[0]
    bids = ast.literal_eval(data[1])
    asks = ast.literal_eval(data[2])

    bids = [[float(elem) for elem in bid] for bid in bids]
    asks = [[float(elem) for elem in ask] for ask in asks]

    conn.close()
    return lastUpdateId, bids, asks

# Fetch an orderbook from the db
def getOrderbook(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, lastUpdateId, bids, asks
                    FROM orderbooks
                    WHERE exchange = ? AND symbol = ?''', (exchange, symbol))

    return cursor.fetchone()

# Fetch a resampled orderbook from the db
def getResampledOrderbook(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, binnedOrderbook
                    FROM resampledOrderbooks
                    WHERE exchange = ? AND symbol = ?''', (exchange, symbol))

    return cursor.fetchone()

# Fetch the latest computed stats from the db
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

# Fetch all computed stats along the time for a given orderbook from the db
def getAllStats(exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, exchange, symbol, totalBidVolume, totalAskVolume
                    FROM stats
                    WHERE exchange = ? AND symbol = ?
                    ORDER BY timestamp
                    ''', (exchange, symbol))

    return cursor.fetchall()