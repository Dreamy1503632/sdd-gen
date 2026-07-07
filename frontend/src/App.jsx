import React, { useState } from "react";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import GeneratePage from "./pages/GeneratePage";
import UploadPage from "./pages/UploadPage";
import SDDPage from "./pages/SDDPage";
import DiagramsPage from "./pages/DiagramsPage";

export default function App() {
  const [activeTab, setActiveTab] = useState("generate");
  const [analysis, setAnalysis] = useState(null);

  const handleAnalysisDone = (result) => {
    setAnalysis(result);
    if (result) setActiveTab("sdd");
  };

  const renderPage = () => {
  switch (activeTab) {
    case "generate": return <GeneratePage />;
    case "upload":   return <UploadPage onAnalysisDone={handleAnalysisDone} />;  // ← fix
    case "sdd":      return <SDDPage hlaSessionId={analysis?.session_id} analysis={analysis} />;
    case "diagrams": return <DiagramsPage analysis={analysis} />;
    default:         return <GeneratePage />;
  }
};

  return (
    <div style={{ minHeight: "100vh", background: "#FFFFFF", fontFamily: "'IBM Plex Sans', 'Segoe UI', sans-serif" }}>
      <link
        href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap"
        rel="stylesheet"
      />
      <Navbar />
      <div style={{ display: "flex", minHeight: "calc(100vh - 60px)" }}>
        <Sidebar
          activeTab={activeTab}
          onTabChange={setActiveTab}
          sddUnlocked={!!analysis}
        />
        <main style={{ flex: 1, minWidth: 0, overflowY: "auto", background: "#FFFFFF", width: "100%" }}>
          {renderPage()}
        </main>
      </div>
    </div>
  );
}