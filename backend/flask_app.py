from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
import sys
import subprocess
from pathlib import Path
from api.people_api import people_blueprint
from api.promotions_api import promotions_blueprint
from api.transactions_api import transactions_blueprint
from api.transfers_api import transfers_blueprint
from api.initialize_api import initialize_blueprint

# Create Flask app
app = Flask(__name__)

# Get the absolute path to your project directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create insights directory inside static folder
INSIGHTS_DIR = os.path.join(BASE_DIR, "static", "insights")
os.makedirs(INSIGHTS_DIR, exist_ok=True)

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 3600
    },
    r"/static/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

def run_initialization_scripts():
    """Run all initialization scripts in the specified order"""
    print("Running initialization scripts...")
    
    # Get the absolute path to the root directory using pathlib
    root_dir = Path(__file__).resolve().parent
    
    # Define scripts in order
    ingestion_scripts = [
        'json_loader.py',
        'yaml_loader.py',
        'people_merger.py',
        'promotions_loader.py',
        'transactions_loader.py',
        'transfers_loader.py'
    ]
    
    # Run ingestion scripts
    ingestion_dir = root_dir / 'ingestion'
    print(f"Running scripts from: {ingestion_dir}")
    
    for script in ingestion_scripts:
        script_path = ingestion_dir / script
        try:
            print(f"Running {script}...")
            subprocess.run([sys.executable, str(script_path)], check=True)
            print(f"Completed {script}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {str(e)}")
            raise
    
    # Run database loader
    try:
        storage_dir = root_dir / 'storage'
        db_loader_path = storage_dir / 'database_loader.py'
        print(f"Running database_loader.py from {db_loader_path}...")
        subprocess.run([sys.executable, str(db_loader_path)], check=True)
        print("Completed database_loader.py")
    except subprocess.CalledProcessError as e:
        print(f"Error running database_loader.py: {str(e)}")
        raise

# Register blueprints
app.register_blueprint(people_blueprint, url_prefix="/api/people")
app.register_blueprint(promotions_blueprint, url_prefix="/api/promotions")
app.register_blueprint(transactions_blueprint, url_prefix="/api/transactions")
app.register_blueprint(transfers_blueprint, url_prefix="/api/transfers")
app.register_blueprint(initialize_blueprint, url_prefix="/api/initialize")

# Route to get stored insights
@app.route('/api/insights/<category>', methods=['GET'])
def get_insights(category):
    try:
        filepath = os.path.join(INSIGHTS_DIR, f"{category}_insights.json")
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return jsonify({"error": f"No insights found for {category}"}), 404
            
        with open(filepath, 'r') as f:
            return jsonify(json.load(f))
    except Exception as e:
        print(f"Error reading insights: {str(e)}")
        return jsonify({"error": f"Error reading insights for {category}"}), 500

# Main entry point
if __name__ == "__main__":
    run_initialization_scripts()
    app.run(debug=True)