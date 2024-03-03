import database
import json
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/orderbook/latest', methods=['GET'])
def getLatestOrderbook():
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
def getLatestResampledOrderbook():
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
def getLatestStats():
    exchange = request.args.get('exchange')
    symbol = request.args.get('symbol')

    stats = database.getStats(exchange, symbol)

    if stats == None:
        return jsonify({"error": "No data found for the specified exchange and symbol."}), 404

    timestamp, exchange, symbol, totalBidVolume, totalAskVolume = stats

    statsJson = {
        "exchange": exchange,
        "currencyPair": symbol,
        "timestamp": timestamp,
        "totalBidVolume": totalBidVolume,
        "totalAskVolume": totalAskVolume
    }

    return jsonify(statsJson)

@app.route('/api/statistics/history', methods=['GET'])
def getStatsHistory():
    exchange = request.args.get('exchange')
    symbol = request.args.get('symbol')

    allStats = database.getAllStats(exchange, symbol)

    if allStats == None:
        return jsonify({"error": "No data found for the specified exchange and symbol."}), 404

    allStatsJson = {
    "exchange": allStats[0][1],
    "symbol": allStats[0][2],
    "statistics": [{
        "timestamp": stats[0],
        "totalBidVolume": stats[3],
        "totalAskVolume": stats[4]
    } for stats in allStats]
    }

    return jsonify(allStatsJson)
