# Backend Documentation

## Overview

The Venmito backend processes raw data from various formats (JSON, YAML, XML, CSV) into a structured SQLite database (`venmito.db`) and provides RESTful API endpoints to interact with the data. The backend enables filtering, querying, and deriving insights using Python, Flask, SQLAlchemy, and Pandas.

---

## Project Structure

```
backend/
├── api/              # API endpoints for interacting with data
├── ingestion/        # Scripts for cleaning and transforming raw datasets
├── models/           # Python models representing database schema (SQLAlchemy ORM)
├── storage/          # SQLite database and database loader
├── flask_app.py      # Main entry point for backend
├── .env              # Contains OpenAI API key
└── requirements.txt  # Python dependencies
```

---

## Core Functionalities

### 1. **Data Ingestion**
The `ingestion/` folder contains scripts for processing raw datasets into cleaned CSVs:
- **`json_loader.py`**: Cleans and converts JSON files into CSV format.
- **`yaml_loader.py`**: Similar to `json_loader.py` but processes YAML files.
- **`people_merger.py`**: Merges cleaned JSON and YAML files into a consolidated `people.csv`.
- **`promotions_loader.py`**: Cleans `promotions.csv` and fills missing data using mapped columns from `people.csv`.
- **`transactions_loader.py`**: Processes raw XML transaction data into structured CSV format.
- **`transfers_loader.py`**: Cleans and processes `transfers.csv`.

### 2. **Database Integration**
The cleaned data is stored in an SQLite database (`venmito.db`) using SQLAlchemy. The `models/` folder contains Python classes that represent the database schema, allowing seamless interaction with the database using the SQLAlchemy ORM.

The schema includes:
- **`people.py`**: Defines the `people` table and its attributes, including relationships with other tables.
- **`promotions.py`**: Represents the `promotions` table for tracking client promotions.
- **`transactions.py`**: Models the `transactions` table for recording customer purchases.
- **`transfers.py`**: Represents the `transfers` table for tracking money transfers between clients.

### 3. **API Endpoints**
API endpoints enable interaction with the data and insights generation. All endpoints are registered via Flask Blueprints located in the `api/` folder.

#### **People API**
- **`GET /api/people/filter`**: Displays and filters the `people` table by parameters such as name, city, country, and device.
- **`GET /api/people/stats`**: Provides statistics on:
  - **Country Distribution**: Number of clients in each country.
  - **Device Ownership**: Distribution of devices used by clients.

#### **Promotions API**
- **`GET /api/promotions/filter`**: Displays and filters the `promotions` table by various criteria.
- **`GET /api/promotions/stats`**: Retrieves insights on:
  - **Country Acceptance Rate**: Percentage of promotions accepted in each country.
- **`GET /api/promotions/stats/promotions`**: Lists promotion items ordered by their acceptance rate in descending order.

#### **Transactions API**
- **`GET /api/transactions/filter`**: Displays and filters the `transactions` table.
- **`GET /api/transactions/stats/customers`**: Ranks customers by their total spending in descending order.
- **`GET /api/transactions/stats/stores`**: Ranks stores by profitability in descending order.
- **`GET /api/transactions/stats/spending_by_country`**: Shows the country distribution of people who made transactions.

#### **Transfers API**
- **`GET /api/transfers/filter`**: Displays and filters the `transfers` table using parameters like sender, receiver, and amount.
- **`GET /api/transfers/stats/country_transfers`**: Displays the distribution of transfers by sending and receiving countries.
- **`GET /api/transfers/stats/monthly_totals`**: Provides the total amount of money transferred per month.

#### **Initialization API**
- **`POST /api/initialize/customers`**: Generates insights for the `customers` table, such as demographic distributions.
- **`POST /api/initialize/promotions`**: Generates insights for the `promotions` table, including acceptance statistics.
- **`POST /api/initialize/transactions`**: Generates insights for the `transactions` table, such as customer spending trends.
- **`POST /api/initialize/transfers`**: Generates insights for the `transfers` table, such as country-wise transfer data.

---

## Setup Instructions

### Prerequisites
- **Python 3.8+**
- Required Python libraries (listed in `requirements.txt`)

### Steps to Run the Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the backend:
   ```bash
   python flask_app.py
   ```

This will:
- Execute ingestion scripts to process raw data.
- Populate the SQLite database.
- Start the Flask server at `http://127.0.0.1:5000`.

---

## API Documentation

Here is a quick reference for the available API endpoints:

| **API**         | **Endpoint**                               | **Description**                                                                            |
|-----------------|-------------------------------------------|-------------------------------------------------------------------------------------------|
| **People**      | `/api/people/filter`                     | Displays and filters the `people` table.                                                 |
|                 | `/api/people/stats`                      | Returns country distribution and device ownership stats.                                  |
| **Promotions**  | `/api/promotions/filter`                 | Displays and filters the `promotions` table.                                             |
|                 | `/api/promotions/stats`                  | Returns acceptance rate stats by country.                                                |
|                 | `/api/promotions/stats/promotions`       | Ranks promotions by acceptance rate.                                                     |
| **Transactions**| `/api/transactions/filter`               | Displays and filters the `transactions` table.                                           |
|                 | `/api/transactions/stats/customers`      | Ranks customers by total spending.                                                       |
|                 | `/api/transactions/stats/stores`         | Ranks stores by profitability.                                                           |
|                 | `/api/transactions/stats/spending_by_country` | Shows country-wise spending distribution.                                            |
| **Transfers**   | `/api/transfers/filter`                  | Displays and filters the `transfers` table.                                              |
|                 | `/api/transfers/stats/country_transfers` | Displays country-wise transfer stats (sent and received).                                |
|                 | `/api/transfers/stats/monthly_totals`    | Provides total transfer amounts by month.                                                |
| **Initialization**| `/api/initialize/customers`            | Generates customer insights.                                                             |
|                 | `/api/initialize/promotions`             | Generates promotions insights.                                                           |
|                 | `/api/initialize/transactions`           | Generates transactions insights.                                                         |
|                 | `/api/initialize/transfers`              | Generates transfers insights.                                                            |

---

## Future Improvements

- Add Docker support for easier deployment.
- Integrate a more robust database solution (e.g., PostgreSQL).
- Make paths absolute so ingestion scripts can be run individually from `backend/ingestion/`.
