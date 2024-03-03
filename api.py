import database
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/orderbook/latest', methods=['GET'])
def get_orderbook_latest():
    exchange = request.args.get('exchange')
    symbol = request.args.get('symbol')

    orderbook = database.getOrderbook(exchange, symbol)

    if orderbook == None:
        return jsonify({"error": "No data found for the specified exchange and symbol."}), 404

    timestamp, exchange, symbol, bids, asks = orderbook
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
    exchange = request.args.get('exchange')
    symbol = request.args.get('symbol')

    resampledOrderbook = database.getResampledOrderbook(exchange, symbol)

    if resampledOrderbook == None:
        return jsonify({"error": "No data found for the specified exchange and symbol."}), 404

    timestamp, exchange, symbol, bins = resampledOrderbook
    bins = json.loads(bins)

    orderbookJson = {
        "exchange": exchange,
        "currencyPair": symbol,
        "timestamp": timestamp,
        "binedOrderbook": [{"bin": bin, "bidQuantity": bidQuantity, "askQuantity": askQuantity} for bin, bidQuantity, askQuantity in bins]
    }

    return jsonify(orderbookJson)

@app.route('/api/statistics/latest', methods=['GET'])
def get_statistics_latest():
    return 'latest stats'
    #return jsonify(statistics_latest)

@app.route('/api/statistics/history', methods=['GET'])
def get_statistics_history():
    return 'stat history'
    #return jsonify({"message": "History endpoint not implemented yet"})
