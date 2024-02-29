import sqlite3
from datetime import datetime

def createTables(cursor):

    # Create tables if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderBookData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestampIndex INTEGER,
            lastUpdatedIdIndex INTEGER,
            exchange TEXT,
            currencyPair TEXT,
            price REAL,
            quantity REAL,
            type TEXT,
            FOREIGN KEY (timestampIndex) REFERENCES Timestamps(id)
            FOREIGN KEY (lastUpdatedIdIndex) REFERENCES LastUpdateIds(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Timestamps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LastUpdateIds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastUpdateId INTEGER
        )
    ''')

def store(cursor, data, exchange, symbol):
    
    timestamp = datetime.now()
    cursor.execute('''
            INSERT INTO Timestamps (timestamp)
            VALUES (?)
        ''', (timestamp,))
    
    timestampIndex = cursor.lastrowid

    timestamp = datetime.now()
    cursor.execute('''
            INSERT INTO LastUpdateIds (lastUpdateId)
            VALUES (?)
        ''', (data['lastUpdateId'],))
    
    lastUpdatedIdIndex = cursor.lastrowid

    # Insert data into tables
    for bid in data['bids']:
        cursor.execute('''
            INSERT INTO OrderBookData (timestampIndex, lastUpdatedIdIndex, exchange, currencyPair, price, quantity, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestampIndex, lastUpdatedIdIndex, exchange, symbol, float(bid[0]), float(bid[1]), 'bid'))

    for ask in data['asks']:
        cursor.execute('''
            INSERT INTO OrderBookData (timestampIndex, lastUpdatedIdIndex, exchange, currencyPair, price, quantity, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestampIndex, lastUpdatedIdIndex, exchange, symbol, float(ask[0]), float(ask[1]), 'ask'))