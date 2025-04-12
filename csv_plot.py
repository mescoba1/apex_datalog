#!/Users/miguel/homebrew/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import sys

def process_csv(file_path):
    """
    Reads a CSV file into a pandas DataFrame and performs basic processing.

    Args:
    file_path: Path to the CSV file.

    Returns:
    pandas DataFrame: Processed DataFrame.
    """

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path) 

    # Basic data cleaning and exploration (example)
    df.dropna(inplace=True)  # Remove rows with missing values

    # convert datestring to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    #print(df.head())  # Display the first few rows
    #print(df.info())  # Get information about the DataFrame

    return df

def get_midnights (dates):
    midnight_dates = list()

    for date in dates:
        if (((date.hour == 0) or (date.hour == 0)) and date.minute == 0):
            midnight_dates.append(date)

    return midnight_dates

if __name__ == "__main__":
    file_path = sys.argv[1]
    processed_df = process_csv(file_path)

    n = 6 * 24 * 60 # 10 mins * 24 hours * days
    date = processed_df['Date'][-n:]
    ph = processed_df['pH'][-n:]
    alk = processed_df['Alkx4'][-n:]
    ca = processed_df['Cax4'][-n:]
    mag = processed_df['Mgx4'][-n:]
    orp = processed_df['ORP'][-n:]
    tmp = processed_df['Tmp'][-n:]

    ph_ra  = ph.rolling (window=6*12).mean()
    orp_ra = orp.rolling (window=6*12).mean()
    tmp_ra = tmp.rolling (window=6*12).mean()

    #vbars = get_midnights(date)
    #plt.vlines(vbars, linestyle='--', ymin=7.9, ymax=8.5)

    fig, axs = plt.subplots(2, 3)

    axs[0, 0].set_title("pH")
    axs[1, 0].set_title("Alkalinity")
    axs[0, 1].set_title("Calcium")
    axs[1, 1].set_title("Magnesium")
    axs[0, 2].set_title("ORP")
    axs[1, 2].set_title("Temperature")

    date_format = mdates.DateFormatter("%m/%d")
    for ii in range(2):
        for jj in range(3):
            axs[ii,jj].xaxis.set_major_formatter(date_format)

    axs[0, 0].plot(date, ph_ra,  'tab:blue',   label='pH')
    axs[1, 0].plot(date, alk,    'tab:green',  label='Alk')
    axs[0, 1].plot(date, ca,     'tab:orange', label='Ca')
    axs[1, 1].plot(date, mag,    'tab:red',    label='Mag')
    axs[0, 2].plot(date, orp_ra, 'tab:purple', label='ORP')
    axs[1, 2].plot(date, tmp_ra, 'tab:orange', label='Temperature')

    #fig.canvas.set_window_title("RedSea Reefer 300G2+")

    plt.show()