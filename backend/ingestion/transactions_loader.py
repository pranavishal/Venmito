import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET

def load_transactions(filepath):
    """
    Parses transactions.xml and flattens the data into a row-per-item structure.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    rows = []
    for transaction in root.findall("transaction"):
        transaction_id = transaction.get("id")
        phone = transaction.find("phone").text
        store = transaction.find("store").text
        
        # Process each item in the transaction
        for item in transaction.find("items").findall("item"):
            item_name = item.find("item").text
            quantity = int(item.find("quantity").text)
            price_per_item = float(item.find("price_per_item").text)
            total_price = float(item.find("price").text)
            
            rows.append({
                "transaction_id": transaction_id,
                "phone": phone,
                "store": store,
                "item_name": item_name,
                "quantity": quantity,
                "price_per_item": price_per_item,
                "total_price": total_price,
            })

    return pd.DataFrame(rows)

def map_phone_to_customer_id(transactions_df, people_df):
    """
    Maps phone numbers from transactions to customer IDs in the people dataset.
    """
    # Create a lookup dictionary from people_df
    phone_to_id = people_df.set_index("phone")["id"].to_dict()

    # Map phone to customer_id
    transactions_df["customer_id"] = transactions_df["phone"].map(phone_to_id)

    return transactions_df

def save_cleaned_transactions(transactions_df):
    """
    Saves the cleaned transactions to a CSV file.
    """
    output_path = Path("../datasets/processed/transactions_cleaned.csv")
    transactions_df.to_csv(output_path, index=False)
    print(f"\nCleaned transactions data saved to: {output_path}")

if __name__ == "__main__":
    # File paths
    transactions_path = Path("../datasets/raw/transactions.xml")
    people_path = Path("../datasets/processed/people_merged.csv")

    # Load the data
    print("Loading transactions...")
    transactions_df = load_transactions(transactions_path)
    
    print("Loading people data...")
    people_df = pd.read_csv(people_path)

    # Map phone numbers to customer IDs
    print("Mapping phone numbers to customer IDs...")
    transactions_df = map_phone_to_customer_id(transactions_df, people_df)

    # Preview the cleaned transactions
    print("\nCleaned Transactions DataFrame Preview:")
    print(transactions_df.head())

    # Save the cleaned transactions
    save_cleaned_transactions(transactions_df)
