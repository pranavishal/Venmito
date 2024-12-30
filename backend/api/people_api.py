from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, or_, and_, func, case
from sqlalchemy.orm import sessionmaker
from models.people import People
import os

# Set up SQLAlchemy
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../storage/venmito.db"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the blueprint
people_blueprint = Blueprint('people', __name__)

# Endpoint to display all people and perform filtering
@people_blueprint.route('/filter', methods=['GET'])
def filter_people():
    try:
        # Get query parameters
        first_name = request.args.get('first_name', '').lower()
        last_name = request.args.get('last_name', '').lower()
        city = request.args.get('city', '').lower()
        country = request.args.get('country', '').lower()
        devices = request.args.getlist('device')

        # Start building the query
        query = session.query(People)

        # Only apply filters if they are provided (not empty strings)
        if first_name.strip():
            query = query.filter(People.firstName.ilike(f"%{first_name}%"))

        if last_name.strip():
            query = query.filter(People.surname.ilike(f"%{last_name}%"))

        if city.strip():
            query = query.filter(People.city.ilike(f"%{city}%"))

        if country.strip():
            query = query.filter(People.country.ilike(f"%{country}%"))

        # Device filtering - only filter for selected devices
        if devices:
            device_conditions = []
            # Add conditions only for selected devices
            for device in devices:
                if device == "Android":
                    device_conditions.append(People.Android.is_(True))
                elif device == "iPhone":
                    device_conditions.append(People.iPhone.is_(True))
                elif device == "Desktop":
                    device_conditions.append(People.Desktop.is_(True))
            
            # If any devices were selected, apply all conditions
            if device_conditions:
                # Use and_ to require all selected devices to be True
                query = query.filter(and_(*device_conditions))

        # Execute the query
        results = query.all()

        # Serialize the results
        people = [
            {
                "id": person.id,
                "email": person.email,
                "phone": person.phone,
                "firstName": person.firstName,
                "surname": person.surname,
                "city": person.city,
                "country": person.country,
                "Android": person.Android,
                "iPhone": person.iPhone,
                "Desktop": person.Desktop
            }
            for person in results
        ]

        return jsonify(people), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Query stats for people data based on country and device
@people_blueprint.route('/stats', methods=['GET'])
def get_stats():
    try:
        # Get total count for percentages
        total_people = session.query(People).count()

        # Get country stats
        country_stats = session.query(
            People.country,
            func.count(People.id).label('count')
        ).group_by(People.country).all()

        # Get device stats
        total_devices = session.query(
            func.sum(
                case((People.Android.is_(True), 1), else_=0) +
                case((People.iPhone.is_(True), 1), else_=0) +
                case((People.Desktop.is_(True), 1), else_=0)
            )
        ).scalar() or 0

        android_count = session.query(func.count(People.id)).filter(People.Android.is_(True)).scalar()
        iphone_count = session.query(func.count(People.id)).filter(People.iPhone.is_(True)).scalar()
        desktop_count = session.query(func.count(People.id)).filter(People.Desktop.is_(True)).scalar()

        stats = {
            'country_stats': [
                {
                    'country': stat.country or 'Unknown',
                    'count': stat.count,
                    'percentage': round((stat.count / total_people) * 100, 2)
                }
                for stat in country_stats
            ],
            'device_stats': [
                {
                    'device': 'Android',
                    'count': android_count,
                    'percentage': round((android_count / total_devices) * 100, 2) if total_devices > 0 else 0
                },
                {
                    'device': 'iPhone',
                    'count': iphone_count,
                    'percentage': round((iphone_count / total_devices) * 100, 2) if total_devices > 0 else 0
                },
                {
                    'device': 'Desktop',
                    'count': desktop_count,
                    'percentage': round((desktop_count / total_devices) * 100, 2) if total_devices > 0 else 0
                }
            ],
            'total_people': total_people,
            'total_devices': total_devices
        }

        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500