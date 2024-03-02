import snapshots, database, ws, stats, resample
import sqlite3
import asyncio

exchange = 'Binance'
symbol = 'BTCUSDT'

# Example usage:
if __name__ == "__main__":
    
    database.initDatabase()
    
    snapshot, timestamp, lastUpdateId = snapshots.getSnapshot(symbol, 50)

    database.storeOrderbook(snapshot, exchange, symbol, timestamp)

    database.getQuantities(exchange, symbol)

    stats.computeAndStoreStats(exchange, symbol)
    
    """
    print("BINS OF SIZE 100")
    resampledData = resample.resample_data(100)
    print(resampledData) """

    #ws.listenWebsocket(symbol.lower())