import database
import datetime
import logging

# Compute statistics for a given orderbook and store them in the db
async def computeAndStoreStats(exchange, symbol):
    logging.info('Computing stats...')
    _, bids, asks = database.getBidsAsksLists(exchange, symbol)
    
    bidQuantities = [float(bid[1]) for bid in bids]
    askQuantities = [float(ask[1]) for ask in asks]
    
    database.storeStats(round(sum(bidQuantities),10), round(sum(askQuantities),10), exchange, symbol, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))