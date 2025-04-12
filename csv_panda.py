#!/Users/miguel/homebrew/bin/python3

import pandas as pd
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
    print(df.head())  # Display the first few rows
    print(df.info())  # Get information about the DataFrame

    # Example: Calculate summary statistics
    print(df.describe()) 

    return df


if __name__ == "__main__":
    file_path = sys.argv[1]
    processed_df = process_csv(file_path)