import snapshots, database, ws, stats, resample
from api import app
import asyncio
import logging

exchange = 'Binance'
symbol = 'BTCUSDT'

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def streamUpdates(exchange, symbol):
    await ws.connectWebsocket(exchange, symbol)

# Example usage:
if __name__ == "__main__":

    # Create db and tables if they don't exist
    database.initDatabase()
    
    # Fetch orderbook snapshot and store it
    snapshots.getAndStoreSnapshot(exchange, symbol, 20)

    # Compute statistics and store them
    stats.computeAndStoreStats(exchange, symbol)
    
    # Resample the latest orderbook and store it
    resample.resampleAndStore(exchange, symbol, 2)

    #ws.listenWebsocket(exchange, symbol)
    asyncio.run(streamUpdates(exchange, symbol))


    # Init API server
    #app.run()