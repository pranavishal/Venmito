from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.transactions import Transactions
import os

# Set up SQLAlchemy
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../storage/venmito.db"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the blueprint
transactions_blueprint = Blueprint('transactions', __name__)

@transactions_blueprint.route('/filter', methods=['GET'])
def filter_transactions():
    try:
        # Get query parameters
        transaction_id = request.args.get('transaction_id', '').strip()
        customer_id = request.args.get('customer_id', '').strip()
        store = request.args.get('store', '').lower()
        item_name = request.args.get('item_name', '').lower()

        # Start building the query
        query = session.query(Transactions)

        # Filter by transaction_id if provided
        if transaction_id:
            try:
                tid = int(transaction_id)
                query = query.filter(Transactions.transaction_id == tid)
            except ValueError:
                pass

        # Filter by customer_id if provided
        if customer_id:
            try:
                cid = int(customer_id)
                query = query.filter(Transactions.customer_id == cid)
            except ValueError:
                pass

        # Text filters
        if store:
            query = query.filter(Transactions.store.ilike(f"%{store}%"))

        if item_name:
            query = query.filter(Transactions.item_name.ilike(f"%{item_name}%"))

        # Execute query and serialize results
        results = query.all()
        transactions = [
            {
                "id": trans.id,
                "transaction_id": trans.transaction_id,
                "customer_id": trans.customer_id,
                "phone": trans.phone,
                "store": trans.store,
                "item_name": trans.item_name,
                "quantity": trans.quantity,
                "price_per_item": trans.price_per_item,
                "total_price": trans.total_price
            }
            for trans in results
        ]

        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500