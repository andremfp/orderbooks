import database
import pandas as pd

def totalVolume(type):
    return sum(database.getQuantities(type.lower()))

def resample_data(data, binSize):
    # Define price bins using the min and max prices from the data
    bins = range(int(data['price'].iloc[0]), int(data['price'].iloc[-1]) + binSize, binSize)

    # Resample data into price bins and aggregate quantity by sum and count
    resampled_data = data.groupby(pd.cut(data['price'], bins), observed=True).agg({'quantity': ['count', 'sum']})
    
    # Reset the index and rename the columns
    resampled_data.reset_index(inplace=True)
    resampled_data.columns = ['bin', 'count', 'quantity']

    return resampled_data