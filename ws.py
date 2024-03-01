import websocket
import json

def on_message(ws, message):
    print(json.loads(message))
    #last_update_id = order_book['lastUpdateId']
    """ if message['u'] <= last_update_id:
        return  
    if message['U'] <= last_update_id + 1 <= message['u']:
        order_book['lastUpdateId'] = message['u']
        process_updates(message)
    else:
        logging.info('Out of sync, re-syncing...')
        order_book = get_snapshot() """

def on_error(ws, error):
    print(f"Encountered error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    
def listenWebsocket(symbol):
    stream = f'wss://stream.binance.com:9443/ws/{symbol}@depth'
    ws = websocket.WebSocketApp(stream, on_message=on_message, on_open=on_open, on_error=on_error, on_close=on_close)
    ws.run_forever()
