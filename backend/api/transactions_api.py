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

# Endpoint to display all transactions and perform filtering
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

# Endpoint to get transaction statistics by customer
@transactions_blueprint.route('/stats/customers', methods=['GET'])
def get_customer_stats():
    try:
        # Get the total spending for each customer
        customer_spending = session.query(
            Transactions.customer_id,
            func.sum(Transactions.total_price).label('total_spent')
        ).group_by(Transactions.customer_id).\
        order_by(func.sum(Transactions.total_price).desc()).\
        all()

        # Get the favorite item for each customer (By quantity bought)
        customer_favorite_items = session.query(
            Transactions.customer_id,
            Transactions.item_name,
            func.sum(Transactions.quantity).label('total_quantity')
        ).group_by(
            Transactions.customer_id,
            Transactions.item_name
        ).\
        order_by(Transactions.customer_id, func.sum(Transactions.quantity).desc()).\
        distinct(Transactions.customer_id).\
        all()

        # Get the favorite store for each customer (By total money spent)
        customer_favorite_stores = session.query(
            Transactions.customer_id,
            Transactions.store,
            func.sum(Transactions.total_price).label('total_spent')
        ).group_by(
            Transactions.customer_id,
            Transactions.store
        ).\
        order_by(Transactions.customer_id, func.sum(Transactions.total_price).desc()).\
        distinct(Transactions.customer_id, Transactions.store).\
        all()

        # Combine the results
        results = []
        for customer_id, total_spent in customer_spending:
            favorite_item_row = next((row for row in customer_favorite_items if row.customer_id == customer_id), None)
            favorite_store_row = next((row for row in customer_favorite_stores if row.customer_id == customer_id), None)
            if favorite_item_row:
                favorite_item = favorite_item_row.item_name
            else:
                favorite_item = None
            if favorite_store_row:
                favorite_store = favorite_store_row.store
            else:
                favorite_store = None
            results.append({
                'customer_id': customer_id,
                'total_spent': total_spent,
                'favorite_item': favorite_item,
                'favorite_store': favorite_store
            })

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in get_customer_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@transactions_blueprint.route('/stats/stores', methods=['GET'])
def get_store_stats():
    try:
        # Get the total spending for each store
        store_total_spending = session.query(
            Transactions.store,
            func.sum(Transactions.total_price).label('total_money_made')
        ).group_by(Transactions.store).\
        order_by(func.sum(Transactions.total_price).desc()).\
        all()

        # Get the best customer for each store (by total money spent)
        store_best_customers = session.query(
            Transactions.store,
            Transactions.customer_id,
            func.sum(Transactions.total_price).label('customer_total_spent')
        ).group_by(Transactions.store, Transactions.customer_id).\
        order_by(Transactions.store, func.sum(Transactions.total_price).desc()).\
        distinct(Transactions.store).\
        all()

        # Get the best selling product for each store (by total quantity sold)
        store_best_products = session.query(
            Transactions.store,
            Transactions.item_name,
            func.sum(Transactions.quantity).label('total_quantity')
        ).group_by(Transactions.store, Transactions.item_name).\
        order_by(Transactions.store, func.sum(Transactions.quantity).desc()).\
        distinct(Transactions.store).\
        all()

        # Combine the results
        results = []
        for store_row in store_total_spending:
            store = store_row.store
            total_money_made = store_row.total_money_made
            best_customer_row = next((row for row in store_best_customers if row.store == store), None)
            if best_customer_row:
                best_customer = best_customer_row.customer_id
            else:
                best_customer = None
            best_product_row = next((row for row in store_best_products if row.store == store), None)
            if best_product_row:
                best_selling_product = best_product_row.item_name
            else:
                best_selling_product = None
            results.append({
                'store': store,
                'best_customer': best_customer,
                'best_selling_product': best_selling_product, 
                'total_money_made': total_money_made
            })

        return jsonify(sorted(results, key=lambda x: x['total_money_made'], reverse=True)), 200

    except Exception as e:
        print(f"Error in get_store_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Endpoint to get spending statistics by country
@transactions_blueprint.route('/stats/spending_by_country', methods=['GET'])
def get_spending_by_country():
    try:
        # Get total spending by country
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
