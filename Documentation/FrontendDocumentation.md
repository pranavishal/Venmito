# Frontend Documentation

## Overview

The Venmito frontend is built with React and serves as the user interface for presenting data from the backend. It enables users to visualize and interact with data through charts, graphs, and tables. The frontend communicates with the backend via REST APIs using `fetch` and `axios` for data retrieval.

---

## Project Structure

```
frontend/
├── components/        # Reusable UI components
│   ├── Navbar.jsx      # Navigation bar for the app
│   ├── BarChart.jsx    # Component for bar chart visualizations
│   ├── LineGraph.jsx   # Component for line graph visualizations
│   ├── PieChart.jsx    # Component for pie chart visualizations
│   ├── StatTable.jsx   # Component for ranking tables
│   └── Table.jsx       # Component for displaying and filtering data tables
├── pages/             # Individual pages of the application
│   ├── LandingPage.jsx # Home page with navigation and summaries
│   ├── PeoplePage.jsx  # Page for client data visualization and filtering
│   ├── PromotionsPage.jsx # Page for promotions data visualization and insights
│   ├── TransactionsPage.jsx # Page for transaction data visualization and insights
│   ├── TransfersPage.jsx # Page for transfer data visualization and insights
│   └── InsightsPage.jsx # Page for AI-generated insights and summaries
├── App.jsx            # Main entry point for the React app
└── index.js           # Renders the React app
```

---

## Core Functionalities

### 1. **Data Visualization**
The frontend provides various components for data visualization:
- **BarChart.jsx**: Displays data as bar charts.
- **PieChart.jsx**: Displays data as pie charts.
- **LineGraph.jsx**: Displays data as line graphs.

These components use `react-chartjs-2` for rendering interactive and dynamic visualizations. The charts dynamically update based on the data fetched from the backend.

### 2. **Data Tables**
- **Table.jsx**: Used to display and filter data in a tabular format.
- **StatTable.jsx**: Specifically designed to rank data by a given attribute (e.g., customer spending, promotion acceptance rates).

### 3. **Pages**
Each page focuses on a specific dataset or functionality:
- **LandingPage.jsx**:
  - Provides an overview of the platform’s features.
  - Contains navigation links to other sections.

- **PeoplePage.jsx**:
  - Fetches and displays client data from `/api/people/filter` and `/api/people/stats`.
  - Includes filtering by name, city, country, and device.
  - Visualizations include:
    - Pie chart for client distribution by country.
    - Pie chart for device ownership breakdown.

- **PromotionsPage.jsx**:
  - Fetches data from `/api/promotions/filter`, `/api/promotions/stats`, and `/api/promotions/stats/promotions`.
  - Includes filtering by promotion type and email.
  - Visualizations include:
    - Bar chart for promotion acceptance rate by country.
    - Ranked table for promotion item acceptance rates.

- **TransactionsPage.jsx**:
  - Fetches data from `/api/transactions/filter`, `/api/transactions/stats/customers`, `/api/transactions/stats/stores`, and `/api/transactions/stats/spending_by_country`.
  - Includes filtering by transaction ID, customer ID, store, and item name.
  - Visualizations include:
    - Pie chart for spending distribution by country.
    - Ranked tables for customer spending and store revenue.

- **TransfersPage.jsx**:
  - Fetches data from `/api/transfers/filter`, `/api/transfers/stats/country_transfers`, and `/api/transfers/stats/monthly_totals`.
  - Includes filtering by sender, recipient, and date range.
  - Visualizations include:
    - Pie charts for money sent and received by country.
    - Line graph for total money sent per month.

- **InsightsPage.jsx**:
  - Fetches AI-generated insights from the backend via `/api/initialize/*` endpoints.
  - Displays categorized insights (e.g., customer trends, promotion insights).

---

## Setup Instructions

### Prerequisites
- **Node.js** (v18 or newer)
- **npm** or **yarn** for package management

### Steps to Run the Frontend
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:5173`.

---

## Technology Stack

- **React**: Component-based library for building user interfaces.
- **React Router**: For client-side routing.
- **Chart.js (via react-chartjs-2)**: For dynamic chart visualizations.
- **Axios**: For making HTTP requests to the backend.
- **Tailwind CSS**: Utility-first CSS framework for responsive and consistent styling.

---

## Future Improvements
- Incorporate responsive design into the frontend.
- Optimize API calls for faster data fetching and caching.
- Add unit tests for components and pages to ensure robustness.
