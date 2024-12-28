from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, or_, and_
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