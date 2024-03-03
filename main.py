import snapshots, database, ws, stats, resample
from api import app

exchange = 'Binance'
symbol = 'BTCUSDT'

# Example usage:
if __name__ == "__main__":

    database.initDatabase()
    
    snapshot, timestamp, lastUpdateId = snapshots.getSnapshot(symbol, 20)

    database.storeOrderbook(snapshot, exchange, symbol, timestamp)

    stats.computeAndStoreStats(exchange, symbol)
    resample.resampleAndStore(exchange, symbol, 2)

    app.run()

    #ws.listenWebsocket(symbol.lower())