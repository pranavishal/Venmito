from flask import Flask
from flask_cors import CORS
from api.people_api import people_blueprint
from api.promotions_api import promotions_blueprint
from api.transactions_api import transactions_blueprint
from api.transfers_api import transfers_blueprint

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:5173",  # Your React dev server
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Register blueprints
app.register_blueprint(people_blueprint, url_prefix="/api/people")
app.register_blueprint(promotions_blueprint, url_prefix="/api/promotions")
app.register_blueprint(transactions_blueprint, url_prefix="/api/transactions")
app.register_blueprint(transfers_blueprint, url_prefix="/api/transfers")

if __name__ == "__main__":
    app.run(debug=True)
