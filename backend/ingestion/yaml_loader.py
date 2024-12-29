import yaml
from pathlib import Path
import pandas as pd

def load_yaml_file(filepath):
    with open(filepath, "r") as file:
        # Load the YAML file directly into a list
        data = yaml.safe_load(file)
    return data  # Return the list of dictionaries directly

def yaml_to_dataframe(data):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Split the `name` column into `firstName` and `surname`
    df[["firstName", "surname"]] = df["name"].str.split(" ", expand=True)
    df.drop(columns=["name"], inplace=True)

    # Split the `city` column into `city` and `country` based on the comma
    df[["city", "country"]] = df["city"].str.split(",", expand=True)
    df["city"] = df["city"].str.strip()  # Remove extra whitespace
    df["country"] = df["country"].str.strip()

    # Convert device fields (Android, Desktop, Iphone) to True/False
    device_columns = ["Android", "Desktop", "Iphone"]
    for col in device_columns:
        df[col] = df[col].astype(bool)

    return df

if __name__ == "__main__":
    filepath = Path("datasets/raw/people.yml")

    # Load and process the YAML data
    people_data = load_yaml_file(filepath)
    people_df = yaml_to_dataframe(people_data)

    # Save the processed data to a CSV file
    output_path = Path("datasets/processed/people_cleaned_yml.csv")
    people_df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
