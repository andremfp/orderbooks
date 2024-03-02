import database
import datetime

def computeAndStoreStats(exchange, symbol):
    bids, asks = database.getBidsAsksLists(exchange, symbol)
    
    bidQuantities = [float(bid[1]) for bid in bids]
    askQuantities = [float(ask[1]) for ask in asks]
    
    print("TOTAL BID,ASK VOLUME")
    print(f'({sum(bidQuantities)},{sum(askQuantities)})')
    database.storeStats(sum(bidQuantities), sum(askQuantities), exchange, symbol, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))