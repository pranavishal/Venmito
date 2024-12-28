from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, or_, and_, func, case
from sqlalchemy.orm import sessionmaker
from models.promotions import Promotions
from models.people import People
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

@promotions_blueprint.route('/stats', methods=['GET'])
def get_promotion_stats():
    try:
        # Get response rate by country
        country_response_rates = session.query(
            People.country,
            func.count(Promotions.id).label('total_promotions'),
            func.sum(
                case(
                    (Promotions.responded == 'Yes', 1),
                    else_=0
                )
            ).label('accepted_promotions')
        ).join(
            Promotions,
            People.email == Promotions.client_email
        ).group_by(
            People.country
        ).all()

        # Calculate percentages and format response
        country_stats = []
        for country, total, accepted in country_response_rates:
            if total > 0:  # Avoid division by zero
                response_rate = (accepted / total) * 100
                country_stats.append({
                    'country': country or 'Unknown',
                    'total_promotions': total,
                    'accepted_promotions': accepted,
                    'response_rate': round(response_rate, 2)
                })

        # Overall promotion statistics
        overall_stats = session.query(
            func.count(Promotions.id).label('total_promotions'),
            func.sum(
                case(
                    (Promotions.responded == 'Yes', 1),
                    else_=0
                )
            ).label('total_accepted'),
            func.count(func.distinct(Promotions.promotion)).label('unique_promotions')
        ).first()

        return jsonify({
            'country_stats': country_stats,
            'overall_stats': {
                'total_promotions': overall_stats[0],
                'total_accepted': overall_stats[1],
                'unique_promotions': overall_stats[2],
                'overall_response_rate': round(
                    (overall_stats[1] / overall_stats[0] * 100), 2
                ) if overall_stats[0] > 0 else 0
            }
        }), 200

    except Exception as e:
        print(f"Error in get_promotion_stats: {str(e)}")  # For debugging
        return jsonify({"error": str(e)}), 500

