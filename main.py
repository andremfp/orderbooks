import snapshots, database, ws, stats, resample
from api import app

exchange = 'Binance'
symbol = 'BTCUSDT'

# Example usage:
if __name__ == "__main__":

    # Create db and tables if they don't exist
    database.initDatabase()
    
    # Fetch orderbook snapshot and store it
    lastUpdateId = snapshots.getAndStoreSnapshot(exchange, symbol, 20)

    # Compute statistics and store them
    stats.computeAndStoreStats(exchange, symbol)
    
    # Resample the latest orderbook and store it
    resample.resampleAndStore(exchange, symbol, 2)

    # Init API server
    app.run()

    #ws.listenWebsocket(symbol.lower())