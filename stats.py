import database
import pandas as pd

def totalVolume():
    bidQuantities, askQuantities = database.getQuantities()
    return sum(bidQuantities), sum(askQuantities)

def resample_data(binSize):

    data = database.getDataToResample()

    # Define price bins using the min and max prices from the data
    bins = range(int(data['price'].iloc[0]), int(data['price'].iloc[-1]) + binSize, binSize)

    # Resample data into price bins and aggregate quantity by sum and count
    resampled_data = data.groupby([pd.cut(data['price'], bins), 'type'], observed=True)['quantity'].sum().unstack(fill_value=0)

    # Reset the index and rename the columns
    resampled_data.reset_index(inplace=True)
    resampled_data.columns = ['bin', 'askQuantity', 'bidQuantity']

    return resampled_data