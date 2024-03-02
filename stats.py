import database
import datetime

def computeAndStoreStats(exchange, symbol):
    quantities = database.getQuantities()
    totalVolumes = tuple(sum(lst) for lst in quantities)
    print("TOTAL BID,ASK VOLUME")
    print(totalVolumes)
    database.storeStats(totalVolumes, exchange, symbol, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))