import snapshots, database, ws, stats
import sqlite3
import asyncio

exchange = 'Binance'
symbol = 'BTCUSDT'

# Example usage:
if __name__ == "__main__":
    
    database.initDatabase()
    
    snapshot = snapshots.getSnapshot(symbol, 1000)
    #print("Order Book Snapshot:")
    #print(snapshot)

    database.store(snapshot, exchange, symbol)

    print('ASKS TO RESAMPLE')
    asks = database.getDataToResample('asks')
    print(asks)

    print("BINS OF SIZE 100")
    resampled_asks = stats.resample_data(asks, 100)
    print(resampled_asks)

    #ws.listenWebsocket(symbol.lower())