import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import LandingPage from "./pages/LandingPage";
import PeoplePage from "./pages/PeoplePage";
import PromotionsPage from "./pages/PromotionsPage";
import TransactionsPage from "./pages/TransactionsPage";
import TransfersPage from "./pages/TransfersPage";
import InsightsPage from "./pages/InsightsPage";

// App component to load all the routes
export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/people" element={<PeoplePage />} />
        <Route path="/promotions" element={<PromotionsPage />} />
        <Route path="/transactions" element={<TransactionsPage />} />
        <Route path="/transfers" element={<TransfersPage />} />
        <Route path="/insights" element={<InsightsPage />} />
      </Routes>
    </Router>
  );
}
