import time
import requests
import socket
import json

def getSnapshot(symbol, limit):
    # Define Binance API URL for order book endpoint
    url = f'https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}'
    
    try:
        # Send GET request to Binance API
        response = requests.get(url)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            return response.json()
        else:
            # Print error message if request failed
            print(f"Failed to fetch order book snapshot. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Print error message if an exception occurred
        print(f"An error occurred: {str(e)}")
        return None