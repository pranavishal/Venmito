from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.transfers import Transfers
from datetime import datetime
import os

# Set up SQLAlchemy
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../storage/venmito.db"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the blueprint
transfers_blueprint = Blueprint('transfers', __name__)

@transfers_blueprint.route('/filter', methods=['GET'])
def filter_transfers():
    try:
        # Get query parameters
        sender_id = request.args.get('sender_id', '').strip()
        recipient_id = request.args.get('recipient_id', '').strip()
        date_after = request.args.get('date_after', '').strip()
        date_before = request.args.get('date_before', '').strip()

        # Start building the query
        query = session.query(Transfers)

        # Filter by sender_id if provided
        if sender_id:
            try:
                sid = int(sender_id)
                query = query.filter(Transfers.sender_id == sid)
            except ValueError:
                pass

        # Filter by recipient_id if provided
        if recipient_id:
            try:
                rid = int(recipient_id)
                query = query.filter(Transfers.recipient_id == rid)
            except ValueError:
                pass

        # Handle date filtering
        if date_after:
            try:
                after_date = datetime.strptime(date_after, '%Y-%m-%d').date()
                query = query.filter(Transfers.date >= after_date)
            except ValueError:
                pass

        if date_before:
            try:
                before_date = datetime.strptime(date_before, '%Y-%m-%d').date()
                query = query.filter(Transfers.date <= before_date)
            except ValueError:
                pass

        # Execute query and serialize results
        results = query.all()
        transfers = [
            {
                "transfer_id": transfer.transfer_id,
                "sender_id": transfer.sender_id,
                "recipient_id": transfer.recipient_id,
                "amount": transfer.amount,
                "date": transfer.date.isoformat() if transfer.date else None
            }
            for transfer in results
        ]

        return jsonify(transfers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500