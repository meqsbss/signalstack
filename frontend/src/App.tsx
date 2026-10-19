import { BrowserRouter, Route, Routes } from "react-router-dom";
import Shell from "./components/Shell";
import CompetitorsPage from "./pages/CompetitorsPage";
import BriefingPage from "./pages/BriefingPage";
import NotFoundPage from "./pages/NotFoundPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Shell />}>
          <Route path="/" element={<CompetitorsPage />} />
          <Route path="/briefing" element={<BriefingPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}