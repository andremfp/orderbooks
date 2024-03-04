import database, snapshots
import websocket
import json

def on_message(ws, message, exchange, symbol):
    updates = json.loads(message)
    snapshots.processUpdates(updates, exchange, symbol)

def on_open(ws):
    print("Connection opened")

def on_error(ws, error):
    print(f"Encountered error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_ping(ws, message):
    print("Got a ping! A pong reply has already been automatically sent.")

def on_pong(ws, message):
    print("Got a pong! No need to respond")
    
def listenWebsocket(exchange, symbol):
    stream = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth'

    def onMessageWrapper(ws, message):
        return on_message(ws, message, exchange, symbol)

    ws = websocket.WebSocketApp(stream, 
                                on_message=onMessageWrapper,
                                on_open=on_open,
                                on_error=on_error,
                                on_close=on_close,
                                on_ping=on_ping,
                                on_pong=on_pong)
    ws.run_forever()