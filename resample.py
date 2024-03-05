import database
import pandas as pd
import datetime
import logging

# Resample an orderbok into bins of size binSize and store it to the db
async def resampleAndStore(exchange, symbol, binSize):
    logging.info('Resampling orderbook...')
    _, bids, asks = database.getBidsAsksLists(exchange, symbol)

    data = buildDataFrame(bids, asks)

    # Define price bins using the min and max prices from the data
    bins = range(int(data['price'].iloc[0]), int(data['price'].iloc[-1]) + binSize, binSize)
    
    # Resample data into price bins and aggregate quantity by sum and count
    resampledData = data.groupby([pd.cut(data['price'], bins), 'type'], observed=True)['quantity'].sum().unstack(fill_value=0)
    
    # Reset the index and rename the columns
    resampledData.reset_index(inplace=True)
    resampledData.columns = ['bin', 'askQuantity', 'bidQuantity']

    resampledOrderbook = buildResampledOrderBook(resampledData)
    database.storeResampledOrderbook(resampledOrderbook, exchange, symbol, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Build a DataFrame with bids and asks
def buildDataFrame(bids, asks):
    bidsDf = pd.DataFrame(bids, columns=['price', 'quantity'])
    bidsDf['type'] = 'bid'  # Add a column indicating it's a bid

    asksDf = pd.DataFrame(asks, columns=['price', 'quantity'])
    asksDf['type'] = 'ask'  # Add a column indicating it's an ask

    # Concatenate bids and asks DataFrames
    data = pd.concat([bidsDf, asksDf], ignore_index=True).sort_values(by='price')

    return data

# Build the resampled orderbook output
def buildResampledOrderBook(resampledData):
    resampledOrderbook = []

    for index, row in resampledData.iterrows():
        # Only want to represent lower bound of the interval
        bin_lower_bound = int(row['bin'].left)

        # Because pandas stores floats as float64, the resulting representation might differ in precision
        # Assuming that quantities don't have more than 10 decimal places
        bin = [
            bin_lower_bound,
            round(row['bidQuantity'],10),
            round(row['askQuantity'],10)
        ]
        
        resampledOrderbook.append(bin)

    return resampledOrderbook