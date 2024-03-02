import time
import sqlite3
import pandas as pd

db = 'orderbook.db'

def initDatabase():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Table for bids
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY,
            timestamp FLOAT,
            exchange TEXT,
            symbol TEXT,
            price REAL,
            quantity REAL
        )
    ''')

    # Table for asks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asks (
            id INTEGER PRIMARY KEY,
            timestamp FLOAT,
            exchange TEXT,
            symbol TEXT,
            price REAL,
            quantity REAL
        )
    ''')

    # Table for last update
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lastUpdate (
            id INTEGER PRIMARY KEY,
            lastUpdateId INTEGER
        )
    ''')

def store(data, exchange, symbol):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    timestamp = time.time()

    # Clear if existing and insert data into tables
    cursor.execute('DELETE FROM lastUpdate')
    cursor.execute('''
            INSERT INTO LastUpdate (lastUpdateId)
            VALUES (?)
        ''', (data['lastUpdateId'],))

    cursor.execute('DELETE FROM bids')
    for bid in data['bids']:
        cursor.execute('''
            INSERT INTO Bids (timestamp, exchange, symbol, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, exchange, symbol, float(bid[0]), float(bid[1])))

    cursor.execute('DELETE FROM asks')
    for ask in data['asks']:
        cursor.execute('''
            INSERT INTO Asks (timestamp, exchange, symbol, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, exchange, symbol, float(ask[0]), float(ask[1])))

    conn.commit()
    conn.close()

def getQuantities(type):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f'SELECT quantity FROM {type}')
    quantities = [row[0] for row in cursor.fetchall()]

    conn.close()
    return quantities

# Function to fetch data from SQLite database
def getDataToResample(type):
    conn = sqlite3.connect(db)
    
    data = pd.read_sql_query(f'SELECT price, quantity FROM {type} ORDER BY price', conn)
    
    conn.close()
    return data
