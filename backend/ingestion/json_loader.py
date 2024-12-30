import json
from pathlib import Path
import pandas as pd

# Loads the Data
def load_json_file(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data

# Converts JSON data to a DataFrame
def json_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

# Checks for Missing Values
def check_missing_values(df):
    print("\nMissing Values by Column:")
    print(df.isnull().sum())

# Normalizes the "location" dictionary to separate "City" and "Country" columns
def normalize_location(df):
    # Normalize the "location" dictionary to separate "City" and "Country" columns
    df[["City", "Country"]] = pd.json_normalize(df["location"])
    df.drop(columns=["location"], inplace=True)
    return df

# Normalizes the "devices" list to one-hot encoding (boolean columns)
def normalize_devices(df):
    # Convert devices list to one-hot encoding (boolean columns)
    devices_df = pd.json_normalize(
        df["devices"].apply(lambda x: {device: True for device in x})
    ).fillna(False)

    df = pd.concat([df, devices_df], axis=1)
    df.drop(columns=["devices"], inplace=True)
    return df

# Main function to run the script
if __name__ == "__main__":
    filepath = Path("datasets/raw/people.json")
    data = load_json_file(filepath)
    people_df = json_to_dataframe(data)
    check_missing_values(people_df)
    people_df = normalize_location(people_df)
    people_df = normalize_devices(people_df)
    # Print the updated DataFrame to verify the changes
    print("\nFinal Normalized Dataframe:")
    print(people_df.head())
    output_path = Path("datasets/processed/people_cleaned_json.csv")
    people_df.to_csv(output_path, index=False)
