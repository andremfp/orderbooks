import database
import datetime

# Compute statistics for a given orderbook and store them in the db
def computeAndStoreStats(exchange, symbol):
    bids, asks = database.getBidsAsksLists(exchange, symbol)
    
    bidQuantities = [float(bid[1]) for bid in bids]
    askQuantities = [float(ask[1]) for ask in asks]
    
    database.storeStats(sum(bidQuantities), sum(askQuantities), exchange, symbol, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))