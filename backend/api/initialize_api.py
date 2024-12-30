from openai import OpenAI
import json
from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI API client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
initialize_blueprint = Blueprint('initialize', __name__)

# OpenAI API endpoint for generating insights on customer data from results in people and transaction pages
@initialize_blueprint.route('/customers', methods=['POST'])  
def analyze_customers():
    try:
        # Fetch only customer-relevant data
        people = requests.get("http://127.0.0.1:5000/api/people/filter").json()
        people_stats = requests.get("http://127.0.0.1:5000/api/people/stats").json()
        transactions_customers = requests.get("http://127.0.0.1:5000/api/transactions/stats/customers").json()
        
        # Prepare data for the GPT-4 model
        data = {
            "people": people,
            "stats": {
                "people": people_stats,
                "transactions_customers": transactions_customers
            },
            "mappings": {
                "People.id": "Primary identifier for customer analysis"
            }
        }

        # Generate insights using the GPT-4 model
        prompt = f"""
        You are analyzing customer data for Venmito, a payment company. Based on the provided data, generate insights about:
        
        Customer trends by country, device usage, and identify growth opportunities. From the data, try and provide useful advice to further grow the company.

        Data:
        {json.dumps(data, indent=2)}

        Output actionable insights in clear, concise sentences. Use this format:
        - [Topic]: [Insight]
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        insights = response.choices[0].message.content

        return jsonify({"insights": insights}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch customer data", "details": str(e)}), 503
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON in customer data response", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error analyzing customer data", "details": str(e)}), 500

# OpenAI API endpoint for generating insights on promotion data from results in promotions page
@initialize_blueprint.route('/promotions', methods=['POST'])  # Changed from /analyze/promotions
def analyze_promotions():
    try:
        promotions = requests.get("http://127.0.0.1:5000/api/promotions/filter").json()
        promotions_stats = requests.get("http://127.0.0.1:5000/api/promotions/stats").json()
        promotions_stats_promotions = requests.get("http://127.0.0.1:5000/api/promotions/stats/promotions").json()

        data = {
            "promotions": promotions,
            "stats": {
                "overall": promotions_stats,
                "promotions": promotions_stats_promotions
            },
            "mappings": {
                "Promotions.recipient_id -> People.id": "Maps promotion recipients to people"
            }
        }

        prompt = f"""
        You are analyzing promotion data for Venmito, a payment company. Based on the provided data, generate insights about:
        
        Most successful promotions, underperforming promotions, country trends, and strategies to increase user acceptance. From the data, try and provide useful advice to further grow the company.

        Data:
        {json.dumps(data, indent=2)}

        Output actionable insights in clear, concise sentences. Use this format:
        - [Topic]: [Insight]
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        insights = response.choices[0].message.content

        return jsonify({"insights": insights}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch promotions data", "details": str(e)}), 503
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON in promotions data response", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error analyzing promotions data", "details": str(e)}), 500

# OpenAI API endpoint for generating insights on transaction data from results in transactions page
@initialize_blueprint.route('/transactions', methods=['POST'])  # Changed from /analyze/transactions
def analyze_transactions():
    try:
        transactions = requests.get("http://127.0.0.1:5000/api/transactions/filter").json()
        transactions_customers = requests.get("http://127.0.0.1:5000/api/transactions/stats/customers").json()
        transactions_stores = requests.get("http://127.0.0.1:5000/api/transactions/stats/stores").json()
        transactions_country = requests.get("http://127.0.0.1:5000/api/transactions/stats/spending_by_country").json()

        data = {
            "transactions": transactions,
            "stats": {
                "customers": transactions_customers,
                "stores": transactions_stores,
                "spending_by_country": transactions_country
            },
            "mappings": {
                "Transactions.customer_id -> People.id": "Maps customers to transactions"
            }
        }

        prompt = f"""
        You are analyzing transaction data for Venmito, a payment company. Based on the provided data, generate insights about:
        
        Most profitable stores, top customers, and revenue distribution by region. From the data, provide useful advice to further grow the company through items to promote, or stores to keep partnerships with.

        Data:
        {json.dumps(data, indent=2)}

        Output actionable insights in clear, concise sentences. Use this format:
        - [Topic]: [Insight]
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        insights = response.choices[0].message.content

        return jsonify({"insights": insights}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch transactions data", "details": str(e)}), 503
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON in transactions data response", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error analyzing transactions data", "details": str(e)}), 500

# OpenAI API endpoint for generating insights on transfer data from results in transfers page
@initialize_blueprint.route('/transfers', methods=['POST'])  # Changed from /analyze/transfers
def analyze_transfers():
    try:
        transfers = requests.get("http://127.0.0.1:5000/api/transfers/filter").json()
        transfers_country = requests.get("http://127.0.0.1:5000/api/transfers/stats/country_transfers").json()
        transfers_monthly = requests.get("http://127.0.0.1:5000/api/transfers/stats/monthly_totals").json()

        data = {
            "transfers": transfers,
            "stats": {
                "country_transfers": transfers_country,
                "monthly_totals": transfers_monthly
            },
            "mappings": {
                "Transfers.sender_id -> People.id": "Maps senders to people",
                "Transfers.recipient_id -> People.id": "Maps recipients to people"
            }
        }

        prompt = f"""
        You are analyzing transfer data for Venmito, a payment company. Based on the provided data, generate insights about:
        
        Countries with highest money movement, sending/receiving patterns, and flow imbalances. From the data, provide useful advice to further grow the company.

        Data:
        {json.dumps(data, indent=2)}

        Output actionable insights in clear, concise sentences. Use this format:
        - [Topic]: [Insight]
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        insights = response.choices[0].message.content

        return jsonify({"insights": insights}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch transfers data", "details": str(e)}), 503
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON in transfers data response", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error analyzing transfers data", "details": str(e)}), 500















