import snapshots, database, ws
import sqlite3
import asyncio

exchange = 'Binance'
symbol = 'BTCUSDT'

# Example usage:
if __name__ == "__main__":
    
    database.initDatabase()
    
    snapshot = snapshots.getSnapshot(symbol)
    print("Order Book Snapshot:")
    print(snapshot)

    database.store(snapshot, exchange, symbol)

    #ws.listenWebsocket(symbol.lower())