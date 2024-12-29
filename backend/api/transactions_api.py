from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, or_, and_, func, case
from sqlalchemy.orm import sessionmaker
from models.transactions import Transactions
from models.people import People
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

@transactions_blueprint.route('/stats/customers', methods=['GET'])
def get_customer_stats():
    try:
        customer_stats = session.query(
            Transactions.customer_id,
            func.sum(Transactions.total_price).label('total_spent'),
            func.max(Transactions.item_name).label('favorite_item'),
            func.max(Transactions.store).label('favorite_store')
        ).group_by(Transactions.customer_id).order_by(
            func.sum(Transactions.total_price).desc()
        ).all()

        results = [
            {
                'customer_id': stat[0],
                'total_spent': stat[1],
                'favorite_item': stat[2],
                'favorite_store': stat[3],
            }
            for stat in customer_stats
        ]

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in get_customer_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@transactions_blueprint.route('/stats/stores', methods=['GET'])
def get_store_stats():
    try:
        store_stats = session.query(
            Transactions.store,
            func.max(Transactions.customer_id).label('best_customer'),
            func.max(People.country).label('best_country'),
            func.sum(Transactions.total_price).label('total_money_made'),
            func.max(Transactions.item_name).label('best_selling_product')
        ).join(People, Transactions.customer_id == People.id).group_by(Transactions.store).order_by(
            func.sum(Transactions.total_price).desc()
        ).all()

        results = [
            {
                'store': stat[0],
                'best_customer': stat[1],
                'total_money_made': stat[3],
                'best_selling_product': stat[4],
            }
            for stat in store_stats
        ]

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in get_store_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@transactions_blueprint.route('/stats/spending_by_country', methods=['GET'])
def get_spending_by_country():
    try:
        spending_stats = session.query(
            func.coalesce(People.country, 'Unknown').label('country'),
            func.sum(func.coalesce(Transactions.total_price, 0)).label('total_spent')
        ).join(People, Transactions.customer_id == People.id, isouter=True).group_by(
            People.country
        ).all()

        print(f"Spending stats query results: {spending_stats}")  # Debugging

        results = [
            {'country': stat[0], 'total_spent': float(stat[1])}
            for stat in spending_stats if stat[1] > 0
        ]

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in get_spending_by_country: {str(e)}")
        return jsonify({"error": str(e)}), 500
