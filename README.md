
# Venmito: Data Engineering Project

## Overview

Venmito is a full-stack data engineering project designed to clean, process, and analyze data from various formats into a structured SQLite database. The project includes a Flask backend for data processing and API handling, and a Vite/React frontend for user interaction and visualization. There is comprehensive documentation in the Documentation folder for both the front-end and back-end.

The project follows a systematic approach:

1. **Data Processing and Cleaning**: Datasets from JSON, YAML, CSV, and XML formats are ingested and cleaned using Python and Pandas. The processed data is saved as structured CSV files.
2. **Database Creation**: The cleaned data is loaded into an SQLite database (`venmito.db`) via SQLAlchemy, creating a relational structure with defined tables and relationships.
3. **Frontend Display with Filtering**: Full data tables are displayed on the React frontend with filtering options by various criteria such as names, devices, and promotions. The frontend incorporates dynamic visualizations like pie charts, bar charts, and line graphs for better data interpretation.
4. **API Endpoints for Additional Insights**: The backend provides RESTful APIs to query data, generate statistics, and derive actionable insights using the OpenAI API for advanced analysis.

The goal is to provide insights about clients, transactions, and promotions by consolidating and querying data from diverse sources such as JSON, YAML, CSV, and XML.

## Features

1. **Data Ingestion and Cleaning**:
   - Processes raw datasets in multiple formats (JSON, YAML, CSV, XML) using Python and Pandas.
   - Cleans and normalizes data, saving processed outputs to CSV files.
   - Please note: The ingestion files rely on relative paths from the root directory because they are invoked by flask_app.py. By default, the processed files and the final database is given. However, if the processed csv files in backend/data/processed (but not the processed folder itself!) and the venmito.db file in backend/storage are removed, they will be automatically regenerated when the backend server (flask_app.py) is run. To test the ingestion files individually, their relative paths must be adjusted accordingly within their respective scripts.

2. **Database Integration**:
   - Consolidates processed data into an SQLite database (`venmito.db`) using SQLAlchemy.
   - Creates Python objects for database tables for seamless queries.

3. **API Endpoints**:
   - Provides RESTful API endpoints for querying and analyzing data.
   - Integrates a Large Language Model (LLM) via the OpenAI API to generate actionable business insights from processed data.
   - Examples include filtering clients and retrieving statistics.

4. **Frontend Features**:
   - Built with React and Vite, styled with Tailwind CSS.
   - Pages for filtering and visualizing data (e.g., using charts for client distributions).

5. **Technology Stack**:
   - Backend:
     - **Flask**: Lightweight framework for building RESTful APIs.
     - **SQLAlchemy**: ORM for interacting with the SQLite database.
     - **SQLite**: Lightweight, file-based relational database.
     - **Pandas**: For data cleaning, processing, and transformation.
     - **OpenAI API**: Used to generate additional insights.
   - Frontend:
     - **React**: Component-based library for building user interfaces.
     - **Vite**: Fast build tool for frontend development.
     - **Tailwind CSS**: Utility-first CSS framework for styling.
     - **Chart.js**: For visualizing data with charts.
     - **React-Router-Dom**: For client-side routing.

## Setup Instructions

### Prerequisites

- **Python 3.8+**
- **Node.js (v18+)** and npm/yarn

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Create a Python virtual environment:
   - **On Mac/Linux**:
     ```bash
     python3 -m venv venv
     ```
   - **On Windows**:
     ```bash
     python -m venv venv
     ```
4. Activate the virtual environment:
   - **On Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **On Windows**:
     ```bash
     venv\Scripts\activate
     ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required dependencies:
   ```bash
   npm install
   ```

### Environment Configuration

This repository includes a .env file that contains the OpenAI API key required for accessing the LLM insights functionality. While including a .env file in a repository is not considered best practice, this project is hosted in a private repository and shared exclusively for evaluation purposes. To use a custom OpenAI API key, follow these steps:

1. Open the .env file located in the backend directory.
2. Replace the existing key with your own OpenAI API key:
   

   OPENAI_API_KEY=your_openai_api_key_here

3. Save the file and restart the backend server to apply the changes.

   
### Running the Project

#### Backend

1. Ensure your Python virtual environment is **activated** (refer to the activation steps above).
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Start the Flask backend:
   ```bash
   python flask_app.py
   ```
4. The backend will be available at:  
   **`http://127.0.0.1:5000`**

#### Frontend

1. Open a new terminal (keep the backend terminal running) and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Start the React frontend:
   ```bash
   npm run dev
   ```
3. The frontend will be available at:  
   **`http://localhost:5173`**

## Usage Instructions

### Backend

1. Run the Flask backend:
   ```bash
   python flask_app.py
   ```
   The backend will be available at `http://127.0.0.1:5000`.

2. Access API endpoints:
   - Example: Filter people by name and location:
     ```bash
     GET /api/people/filter?first_name=John&city=New York
     ```
   - Query insights, e.g., device distribution:
     ```bash
     GET /api/insights/devices
     ```

### Frontend

1. Run the React frontend (in a second terminal). Navigate to the `frontend` directory and run the following command:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

### PLEASE NOTE
When navigating to a page, it may take a few moments for the data to load. If the page appears empty initially, it should populate after a short delay. This is particularly true for the Insights page, which interacts with OpenAI's API. While data is being fetched, a "loading insights" message will be displayed. Please allow a few moments for this process to complete.

## Project Structure

### Backend

- **`flask_app.py`**: Main entry point, initializes data processing and serves APIs.
- **`ingestion/`**: Contains scripts for loading and cleaning raw datasets.
- **`api/`**: Defines API endpoints.
- **`models/`**: SQLAlchemy models for database tables.
- **`storage/`**: Stores the SQLite database and related files.

### Frontend

- **`src/pages/`**: React components for application pages (e.g., PeoplePage, PromotionsPage).
- **`src/components/`**: Reusable components (e.g., Navbar, PieChart).
- **`App.jsx`**: Main application file, defines routes and navigation.

## API Documentation

### People API

1. **Filter People**:
   - Endpoint: `GET /api/people/filter`
   - Query Parameters: `first_name`, `last_name`, `city`, `country`, `device` (array)
   - Example:
     ```bash
     GET /api/people/filter?first_name=Jane&country=USA&device=Android
     ```

2. **Get Statistics**:
   - Endpoint: `GET /api/people/stats`
   - Description: Returns stats on clients, such as device ownership and country distribution.

## Design Decisions

- **SQLite**: Chosen for simplicity and ease of setup.
- **React with Vite**: Enables fast and modular frontend development.
- **Flask**: Lightweight and efficient for API and backend logic.

## Future Improvements

- Improve AI Insights through fine-tuning or an RAG Architecture
- Make front end responsive

---

Developed by Pranav Vishal  
Email: pvishal@uwaterloo.ca
