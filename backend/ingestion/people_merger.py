import pandas as pd
from pathlib import Path

def load_people_files():

    json_path = Path("datasets/processed/people_cleaned_json.csv")
    yml_path = Path("datasets/processed/people_cleaned_yml.csv")

    json_df = pd.read_csv(json_path)
    yml_df = pd.read_csv(yml_path)
    json_df.rename(columns={'telephone': 'phone'}, inplace=True)
    json_df.rename(columns={'last_name': 'surname'}, inplace=True)
    yml_df.columns = yml_df.columns.str.lower().str.replace(' ', '').str.replace('_', '')
    json_df.columns = json_df.columns.str.lower().str.replace(' ', '').str.replace('_', '')

    #print(json_df.head)
    #print(yml_df.head())


    return json_df, yml_df

def merge_people_data(json_df, yml_df):
    merged_df = pd.merge(json_df, yml_df, on='id', how="outer", suffixes=("_json", "_yml"))
    # Resolve conflicts for shared columns
    merged_df['email'] = merged_df['email_json'].combine_first(merged_df['email_yml'])
    merged_df['phone'] = merged_df['phone_json'].combine_first(merged_df['phone_yml'])
    merged_df['city'] = merged_df['city_json'].combine_first(merged_df['city_yml'])
    merged_df['country'] = merged_df['country_json'].combine_first(merged_df['country_yml'])
    merged_df['firstname'] = merged_df['firstname_json'].combine_first(merged_df['firstname_yml'])
    merged_df['surname'] = merged_df['surname_json'].combine_first(merged_df['surname_yml'])
    merged_df['android'] = merged_df['android_json'].combine_first(merged_df['android_yml'])
    merged_df['iphone'] = merged_df['iphone_json'].combine_first(merged_df['iphone_yml'])
    merged_df['desktop'] = merged_df['desktop_json'].combine_first(merged_df['desktop_yml'])

    # Drop redundant columns
    merged_df.drop(columns=[
        'email_json', 'email_yml',
        'phone_json', 'phone_yml',
        'city_json', 'city_yml',
        'country_json', 'country_yml',
        'firstname_json', 'firstname_yml',
        'surname_json', 'surname_yml',
        'android_json', 'android_yml',
        'iphone_json', 'iphone_yml',
        'desktop_json', 'desktop_yml'
    ], inplace=True)

    print(merged_df.head())

    return merged_df

def save_merged_people(merged_df):
    output_path = Path("datasets/processed/people_merged.csv")
    merged_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    json_df, yml_df = load_people_files()
    merged_people_df = merge_people_data(json_df, yml_df)

    save_merged_people(merged_people_df)