import pandas as pd
from pathlib import Path

def load_promotions(filepath):
    df = pd.read_csv(filepath, na_values=[""])
    df.rename(columns={'telephone': 'phone'}, inplace=True)
    return df

def check_missing_and_invalid_values(df):
    print("\nMissing or NaN Values by Column:")
    print(df.isnull().sum())

    # Check for unexpected values in 'responded'
    print("\nUnique Values in 'responded':")
    print(df['responded'].unique())

def clean_promotions_data(promotions_df, people_df):
    promotions_df["client_email"] = promotions_df["client_email"].combine_first(promotions_df["phone"].map(people_df.set_index("phone")["email"]))
    promotions_df["phone"] = promotions_df["phone"].combine_first(promotions_df["client_email"].map(people_df.set_index("email")["phone"]))

    # Print cleaned DataFrame
    print("\nCleaned Promotions DataFrame Preview:")
    print(promotions_df.head())

    return promotions_df

def save_cleaned_promotions(promotions_df):
    output_path = Path("datasets/processed/promotions_cleaned.csv")
    promotions_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    filepath = Path("datasets/raw/promotions.csv")
    promotions_df = load_promotions(filepath)
    
    people_path = Path("datasets/processed/people_merged.csv")
    people_df = pd.read_csv(people_path)

    check_missing_and_invalid_values(promotions_df)

    promotions_df = clean_promotions_data(promotions_df, people_df)

    check_missing_and_invalid_values(promotions_df)
    save_cleaned_promotions(promotions_df)

