import time
import sqlite3

db = 'orderbook.db'

def initDatabase():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for bids
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp FLOAT,
            exchange TEXT,
            symbol TEXT,
            price REAL,
            quantity REAL
        )
    ''')

    # Table for asks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Asks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp FLOAT,
            exchange TEXT,
            symbol TEXT,
            price REAL,
            quantity REAL
        )
    ''')

    # Table for last update
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LastUpdate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastUpdateId INTEGER
        )
    ''')

def store(data, exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    timestamp = time.time()

    # Clear if existing and insert data into tables
    cursor.execute('DELETE FROM LastUpdate')
    cursor.execute('''
            INSERT INTO LastUpdate (lastUpdateId)
            VALUES (?)
        ''', (data['lastUpdateId'],))

    cursor.execute('DELETE FROM Bids')
    for bid in data['bids']:
        cursor.execute('''
            INSERT INTO Bids (timestamp, exchange, symbol, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, exchange, symbol, float(bid[0]), float(bid[1])))

    cursor.execute('DELETE FROM Asks')
    for ask in data['asks']:
        cursor.execute('''
            INSERT INTO Asks (timestamp, exchange, symbol, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, exchange, symbol, float(ask[0]), float(ask[1])))

    conn.commit()
    conn.close()