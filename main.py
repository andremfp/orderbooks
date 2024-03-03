import snapshots, database, ws, stats, resample
import sqlite3
import asyncio

exchange = 'Binance'
symbol = 'BTCUSDT'

# Example usage:
if __name__ == "__main__":
    
    database.initDatabase()
    
    snapshot, timestamp, lastUpdateId = snapshots.getSnapshot(symbol, 20)

    database.storeOrderbook(snapshot, exchange, symbol, timestamp)

    stats.computeAndStoreStats(exchange, symbol)
    resample.resampleAndStore(exchange, symbol, 2)

    #ws.listenWebsocket(symbol.lower())