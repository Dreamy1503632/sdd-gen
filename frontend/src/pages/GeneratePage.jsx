import React, { useState } from "react";
import { INDUSTRIES, HCM_MODULES } from "../lib/constants";
import { generateQuestionnaire } from "../lib/api";
import ModuleSelector from "../components/ModuleSelector";
import { Button, SectionTitle, InfoBox, StatCard, Card } from "../components/UI";

export default function GeneratePage() {
  const [industry, setIndustry] = useState("");
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const ready = industry && modules.length > 0;

  const handleGenerate = async () => {
    if (!ready) return;
    setLoading(true);
    setError(null);
    try {
      await generateQuestionnaire(industry, modules);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "32px 36px" }}>
      <SectionTitle>Generate HLA Questionnaire</SectionTitle>

      <InfoBox title="📊 Industry-Specific Question Bank">
        Generate a tailored Excel questionnaire with priority-rated questions, built-in guidance, and
        comprehensive coverage across all selected modules. Questions span strategic objectives,
        current state, compliance, integrations, and change management.
      </InfoBox>

      <div style={{ marginBottom: 28 }}>
        <div style={{ fontSize: "0.8rem", fontWeight: 700, color: "#0A1628", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 10 }}>
          Industry
        </div>
        <select
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          style={{
            width: "100%",
            maxWidth: 480,
            padding: "12px 16px",
            border: "2px solid #C8E0EC",
            borderRadius: 10,
            fontSize: "0.9rem",
            color: "#0A1628",
            background: "#fff",
            outline: "none",
            cursor: "pointer",
          }}
        >
          <option value="">— Select Industry —</option>
          {INDUSTRIES.map((ind) => (
            <option key={ind} value={ind}>{ind}</option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: 32 }}>
        <div style={{ fontSize: "0.8rem", fontWeight: 700, color: "#0A1628", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 10 }}>
          HCM Modules <span style={{ color: "#4A6A90", fontWeight: 400 }}>(select one or more)</span>
        </div>
        <ModuleSelector selected={modules} onChange={setModules} />
      </div>

      {ready && (
        <Card style={{ marginBottom: 28 }}>
          <div style={{ fontSize: "0.8rem", fontWeight: 700, color: "#0A1628", marginBottom: 16 }}>
            Questionnaire Preview
          </div>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 16 }}>
            <StatCard value={modules.length} label="Modules" />
            <StatCard value={modules.length + 4} label="Excel Sheets" />
            <StatCard value="Critical / High / Med" label="Priority Tiers" accent="#1A5FA8" />
          </div>
          <div style={{ fontSize: "0.82rem", color: "#4A6A90" }}>
            <strong style={{ color: "#0A1628" }}>Industry:</strong> {industry} &nbsp;·&nbsp;{" "}
            <strong style={{ color: "#0A1628" }}>Modules:</strong> {modules.join(", ")}
          </div>
        </Card>
      )}

      {error && (
        <div style={{ background: "#FFF4F4", border: "1px solid #E53935", borderRadius: 8, padding: "12px 16px", color: "#E53935", fontSize: "0.85rem", marginBottom: 16 }}>
          {error}
        </div>
      )}

      <Button variant="accent" onClick={handleGenerate} disabled={!ready || loading}>
        {loading ? "⏳ Generating…" : "📥 Download Excel Questionnaire"}
      </Button>
    </div>
  );
}