import database
import datetime
import requests

def getAndStoreSnapshot(exchange, symbol, limit):
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
            return response.json()['lastUpdateId']
        else:
            # Print error message if request failed
            print(f"Failed to fetch order book snapshot. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Print error message if an exception occurred
        print(f"An error occurred: {str(e)}")
        return None