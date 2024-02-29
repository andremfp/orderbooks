import snapshots, database
import sqlite3
import time
import threading

# Example usage:
if __name__ == "__main__":
    exchange = 'Binance'
    symbol = 'BTCUSDT'
    
    # Connect to SQLite database
    conn = sqlite3.connect('orderbook.db')
    cursor = conn.cursor()

    database.createTables(conn)
    
    snapshot = snapshots.fetch_orderbook_snapshot(symbol)
    print("Order Book Snapshot:")
    print(snapshot)

    database.store(cursor, snapshot, exchange, symbol)

    conn.commit()
    conn.close()