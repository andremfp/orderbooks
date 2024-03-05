import database
import datetime
import requests
import logging

def getAndStoreSnapshot(exchange, symbol, limit):
    logging.info('Getting snapshot...')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Define Binance API URL for order book endpoint
    url = f'https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}'
    
    try:
        # Send GET request to Binance API
        response = requests.get(url)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            
            # Store the orderbook
            database.storeOrderbook(response.json(), exchange, symbol, timestamp)
        else:
            # Print error message if request failed
            logging.fatal(f"Failed to fetch order book snapshot. Status code: {response.status_code}")
    except Exception as e:
        # Print error message if an exception occurred
        logging.fatal(f"An error occurred: {str(e)}")

def processUpdates(updates, exchange, symbol):
    logging.info('Processing updates...')
    lastUpdateId, bids, asks = database.getBidsAsksLists(exchange, symbol)

    # Sort bids and asks by price
    bids = sorted(bids, key=lambda x: x[0])
    asks = sorted(asks, key=lambda x: x[0])
    
    # Not sure if this can happen
    # If snapshot is more recent than the last update, it's of no use
    if updates['u'] <= lastUpdateId:
        logging.info('Stale update. Dropping it...')
        return  
    # If update window contains the snapshot's last update, update local snapshot
    if updates['U'] <= lastUpdateId + 1 <= updates['u']:
        updateSnapshot(updates, lastUpdateId, bids, asks, exchange, symbol)
    # If the snapshot is older than the update window, we need to re-sync and fetch a new snapshot
    else:
        logging.info('Out of sync, re-syncing...')
        getAndStoreSnapshot(exchange, symbol, 20)

def updateSnapshot(updates, lastUpdateId, bids, asks, exchange, symbol):
    logging.info('Updating snapshot...')
    bidUpdates = updates['b']
    askUpdates = updates['a']

    bids = updateOrders(bidUpdates, bids)
    asks = updateOrders(askUpdates, asks)   

    # Store updated snapshot
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.storeUpdatedOrderbook(lastUpdateId, bids, asks, timestamp, exchange, symbol)

def updateOrders(updates, orders):
    lowestOrderPrice = orders[0][0]
    highestOrderPrice = orders[-1][0]

    ordersToAppend = []

    for update in updates:
        # Convert value to float
        update = [float(elem) for elem in update]
        updatePrice, updateQuantity = update

        # If update is outside of the local snapshot, ignore
        if updatePrice < lowestOrderPrice or updatePrice > highestOrderPrice:
            continue

        for i in range(0, len(orders)):
            updated = False
            currOrderPrice = orders[i][0]
            currOrderQuantity = orders[i][1]

            if updatePrice == currOrderPrice:
                updated = True
                # If Quantity is 0, remove from snapshot
                if updateQuantity == 0:
                    orders.pop(i)
                    break
                # No quantity change
                if updateQuantity == currOrderQuantity:
                    break
                # Quantity change, update order
                else:
                    orders[i] = update
                    break

        # If price not found and quantity is not 0, add new order
        if updateQuantity != 0 and updated == False:
            ordersToAppend.append(update)

    # Append new orders at the end to preserver ordered lists before
    # Check if not empty, in the remote possibility that all orders got removed in the update
    if orders:
        for newOrder in ordersToAppend:
            orders.append(newOrder)

    return orders