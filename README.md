# orderbooks

## Introduction

A simple app that collects, processes, stores, and serves real-time orderbook data from cryptocurrency
exchanges.

### Current state

Currently, the app is hardcoded to collect BTCUSDT data from Binance. Can be expanded to more exchanges and symbols.

### Assumptions

- Data from the exchange is not ordered in any way;
- Order quantities do not have more than 10 decimal places;
- Websocket stream updates every second;
- No errors or bad requests occur, as for now, there isn't much error handling;
- Snapshot limit is hardcoded to 1000;
- Resample bin size is hardcoded to 100;
- Timestamps in the databases are from when a given entry was added/computed;
- `exchange` and `symbol` pairs are unique;

## How it works

- Fetches the latest orderbook snapshot for a given `exchange` and `symbol` (currently only `Binance`, `BTCUSDT`);
- Stores this initial snapshot in a local SQLite table;
- Runs a thread that opens a websocket connection to the exchange's stream for the given `symbol`;
- Runs a thread that computes statistics (total volume for now) on the latest stored orderbook every 5 minutes and stores them in order to keep a history;
- Runs a thread that resamples the latest stored orderbook every 10 minutes and stores it, keeping only the latest resample;
- Starts an API server on port 5000 to serve the stored data via the following endpoints:
  - `/api/orderbook/latest?exchange=<exchange>&symbol=<symbol>`
  - `/api/orderbook/resampled?exchange=<exchange>&symbol=<symbol>`
  - `/api/statistics/latest?exchange=<exchange>&symbol=<symbol>`
  - `/api/statistics/history?exchange=<exchange>&symbol=<symbol>`

## Installation

1. Clone the repository;
2. Navigate to the project directory;
3. Install dependencies from requirements.txt: `pip install -r requirements.txt`
4. Run orderbooks.py
