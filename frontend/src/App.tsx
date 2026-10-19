import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ToastProvider } from "./hooks/useToast";
import ToastContainer from "./components/Toast";
import Shell from "./components/Shell";
import CompetitorsPage from "./pages/CompetitorsPage";
import AddCompetitorPage from "./pages/AddCompetitorPage";
import CompetitorDetailPage from "./pages/CompetitorDetailPage";
import BriefingPage from "./pages/BriefingPage";
import NotFoundPage from "./pages/NotFoundPage";

export default function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Shell />}>
            <Route path="/" element={<CompetitorsPage />} />
            <Route path="/add" element={<AddCompetitorPage />} />
            <Route path="/competitor/:id" element={<CompetitorDetailPage />} />
            <Route path="/briefing" element={<BriefingPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <ToastContainer />
    </ToastProvider>
  );
}