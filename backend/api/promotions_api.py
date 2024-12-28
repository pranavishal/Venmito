from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from models.promotions import Promotions
import os

# Set up SQLAlchemy
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../storage/venmito.db"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the blueprint
promotions_blueprint = Blueprint('promotions', __name__)

@promotions_blueprint.route('/filter', methods=['GET'])
def filter_promotions():
    try:
        # Get query parameters
        promotion = request.args.get('promotion', '').lower()
        email = request.args.get('email', '').lower()
        responded = request.args.getlist('responded')  # Will handle like devices

        # Start building the query
        query = session.query(Promotions)

        # Only apply filters if they are provided (not empty strings)
        if promotion.strip():
            query = query.filter(Promotions.promotion.ilike(f"%{promotion}%"))

        if email.strip():
            query = query.filter(Promotions.client_email.ilike(f"%{email}%"))

        # Response filtering - matching database format of "Yes"/"No"
        if responded:
            response_conditions = []
            if "yes" in responded:
                response_conditions.append(Promotions.responded == "Yes")
            if "no" in responded:
                response_conditions.append(Promotions.responded == "No")
            
            if response_conditions:
                query = query.filter(and_(*response_conditions))

        # Execute the query
        results = query.all()

        # Serialize the results
        promotions = [
            {
                "id": promo.id,
                "client_email": promo.client_email,
                "phone": promo.phone,
                "promotion": promo.promotion,
                "responded": promo.responded
            }
            for promo in results
        ]

        return jsonify(promotions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500