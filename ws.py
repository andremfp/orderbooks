import snapshots
import websockets
import json
import logging

async def handleMessages(ws, exchange, symbol):
    async for message in ws:
        logging.info('Got update, processing it')
        updates = json.loads(message)
        snapshots.processUpdates(updates, exchange, symbol)

""" def on_ping(ws, message):
    print("Got a ping! A pong reply has already been automatically sent.")

def on_pong(ws, message):
    print("Got a pong! No need to respond") """

async def connectWebsocket(exchange, symbol):
    stream = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth'
    
    try:
        logging.info('Attempting to open stream connection...')
        async with websockets.connect(stream) as ws:
            # Handle open event
            logging.info('Stream connection opened')

            # Handle incoming messages
            await handleMessages(ws, exchange, symbol)

    except websockets.exceptions.ConnectionClosed as close_event:
        # Handle close event
        logging.info(f"WebSocket connection closed with code {close_event.code}, reason: {close_event.reason}")

    except websockets.exceptions.WebSocketException as error:
        # Handle error event
        logging.info(f"WebSocket error occurred: {error}")