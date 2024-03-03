import database
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Define API endpoints
@app.route('/api/orderbook/latest', methods=['GET'])
def get_orderbook_latest():
    exchange = request.args.get('exchange')
    symbol = request.args.get('symbol')

    orderbook = database.getOrderbook(exchange, symbol)

    if orderbook == None:
        return jsonify({"error": "No data found for the specified exchange and symbol."}), 404

    timestamp, exchange, symbol, bids, asks = database.getOrderbook(exchange, symbol)
    bids = json.loads(bids)
    asks = json.loads(asks)

    orderbookJson = {
        "exchange": exchange,
        "currencyPair": symbol,
        "timestamp": timestamp,
        "bids": [{"price": price, "quantity": quantity} for price, quantity in bids],
        "asks": [{"price": price, "quantity": quantity} for price, quantity in asks]
    }

    return jsonify(orderbookJson)

@app.route('/api/orderbook/resampled', methods=['GET'])
def get_orderbook_resampled():
    return 'latest resampled orderbook'
    #return jsonify(orderbook_latest)

@app.route('/api/statistics/latest', methods=['GET'])
def get_statistics_latest():
    return 'latest stats'
    #return jsonify(statistics_latest)

@app.route('/api/statistics/history', methods=['GET'])
def get_statistics_history():
    return 'stat history'
    #return jsonify({"message": "History endpoint not implemented yet"})
