import pandas as pd
from pathlib import Path

def load_transfers(filepath):
    """
    Loads the transfers CSV file into a Pandas DataFrame.

    Args:
        filepath (str or Path): Path to the transfers CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(filepath)
    return df

def check_transfers_data(transfers_df, people_df):
    """
    Checks the transfers DataFrame for missing values, valid data types,
    and referential integrity with the people DataFrame.

    Args:
        transfers_df (pd.DataFrame): The transfers DataFrame.
        people_df (pd.DataFrame): The people DataFrame.

    Returns:
        None
    """
    # Check for missing values
    print("\nMissing or NaN Values by Column:")
    print(transfers_df.isnull().sum())

    # Validate data types
    print("\nData Types:")
    print(transfers_df.dtypes)

    # Confirm all sender_id and recipient_id exist in people DataFrame
    sender_valid = transfers_df['sender_id'].isin(people_df['id']).all()
    recipient_valid = transfers_df['recipient_id'].isin(people_df['id']).all()

    if sender_valid and recipient_valid:
        print("\nAll sender_id and recipient_id values are valid!")
    else:
        print("\nSome sender_id or recipient_id values are invalid!")

def save_cleaned_transfers(transfers_df):
    output_path = Path("../datasets/processed/transfers_cleaned.csv")
    transfers_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    transfers_path = Path("../datasets/raw/transfers.csv")
    people_path = Path("../datasets/processed/people_merged.csv")

    # Load the data
    transfers_df = load_transfers(transfers_path)
    people_df = pd.read_csv(people_path)

    # Check the transfers data
    print("\nRaw Transfers DataFrame Preview:")
    print(transfers_df.head())

    check_transfers_data(transfers_df, people_df)
    save_cleaned_transfers(transfers_df)