import snapshots, database, ws, stats, resample
from api import app
import asyncio
import logging
import threading
import time

exchange = 'Binance'
symbol = 'BTCUSDT'

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def streamUpdates(exchange, symbol):
    await ws.connectWebsocket(exchange, symbol)

async def statistics(exchange, symbol):
    while True:
        await stats.computeAndStoreStats(exchange, symbol)
        # Sleep for 5 minutes
        time.sleep(5 * 60)

# Example usage:
if __name__ == "__main__":

    # Create db and tables if they don't exist
    database.initDatabase()
    
    # Fetch orderbook snapshot and store it
    snapshots.getAndStoreSnapshot(exchange, symbol, 20)
    
    # Resample the latest orderbook and store it
    resample.resampleAndStore(exchange, symbol, 2)

    # Start webSocket thread
    wsThread = threading.Thread(target=lambda: asyncio.run(streamUpdates(exchange, symbol)))
    wsThread.start()

    # Start statistics thread
    statisticsThread = threading.Thread(target=lambda: asyncio.run(statistics(exchange, symbol)))
    statisticsThread.start()

    # Init API server
    app.run()