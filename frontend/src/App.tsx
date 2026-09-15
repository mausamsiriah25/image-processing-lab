import { Route, Routes } from "react-router-dom";
import AppShell from "./layouts/AppShell";
import HomePage from "./pages/HomePage";
import PracticalsDashboard from "./pages/PracticalsDashboard";
import PracticalDetailPage from "./pages/PracticalDetailPage";
import AboutPage from "./pages/AboutPage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/practicals" element={<PracticalsDashboard />} />
        <Route path="/practicals/:id" element={<PracticalDetailPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route
          path="*"
          element={
            <div className="mx-auto max-w-xl px-4 py-24 text-center">
              <h1 className="text-2xl font-bold">Page not found</h1>
            </div>
          }
        />
      </Route>
    </Routes>
  );
}
