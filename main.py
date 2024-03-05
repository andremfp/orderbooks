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

async def resampleSnapshot(exchange, symbol):
    while True:
        # Resample into bins of 100
        await resample.resampleAndStore(exchange, symbol, 100)
        # Sleep for 10 minutes
        time.sleep(10 * 60)
    

if __name__ == "__main__":

    # Create db and tables if they don't exist
    database.initDatabase()
    
    # Fetch initial orderbook snapshot and store it
    snapshots.getAndStoreSnapshot(exchange, symbol, 1000)

    # Start webSocket thread
    wsThread = threading.Thread(target=lambda: asyncio.run(streamUpdates(exchange, symbol)))
    wsThread.start()

    # Start statistics thread
    statisticsThread = threading.Thread(target=lambda: asyncio.run(statistics(exchange, symbol)))
    statisticsThread.start()

    # Start resample thread
    resampleThread = threading.Thread(target=lambda: asyncio.run(resampleSnapshot(exchange, symbol)))
    resampleThread.start()

    # Init API server
    app.run()