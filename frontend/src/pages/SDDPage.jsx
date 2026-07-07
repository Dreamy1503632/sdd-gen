import React, { useState } from "react";
import { streamSDD, downloadSDD } from "../lib/api";
import { Button, SectionTitle, InfoBox, StatCard, ProgressBar, Card } from "../components/UI";

function ConfigField({ label, value, onChange, placeholder }) {
  return (
    <div>
      <div style={{ fontSize: "0.75rem", fontWeight: 700, color: "#0A1628", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>
        {label}
      </div>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          width: "100%",
          padding: "10px 14px",
          border: "2px solid #C8E0EC",
          borderRadius: 8,
          fontSize: "0.88rem",
          color: "#0A1628",
          outline: "none",
          background: "#fff",
          boxSizing: "border-box",
        }}
      />
    </div>
  );
}

export default function SDDPage({ hlaSessionId, analysis }) {
  const [config, setConfig] = useState({
    company_name: "",
    project_name: "Oracle Fusion HCM Implementation",
    doc_reference: "SDD_V1.0",
    author: "Implementation Team",
    version: "1.0",
    confidentiality: "Confidential",
  });
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState("");
  const [logs, setLogs] = useState([]);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  const set = (k) => (v) => setConfig((p) => ({ ...p, [k]: v }));

  const handleGenerate = () => {
    if (!config.company_name.trim()) { setError("Company name is required."); return; }
    setError(null);
    setGenerating(true);
    setLogs([]);
    setProgress(0);
    setSummary(null);

    streamSDD(
      hlaSessionId,
      config,
      (evt) => {
        setProgress(evt.progress ?? 0);
        setStage(evt.stage ?? "");
        setLogs((p) => [...p, evt.message ?? evt.stage ?? ""]);
        if (evt.status === "complete") {
          setSummary(evt);
          setGenerating(false);
        }
      },
      () => setGenerating(false),
      (e) => { setError(e.message); setGenerating(false); }
    );
  };

  const handleDownload = async () => {
    try {
      await downloadSDD(summary?.session_id ?? hlaSessionId);
    } catch (e) {
      setError(e.message);
    }
  };

  const sddSections = [
    "Chapter 1 · Document Control & Table of Contents",
    "Chapter 2 · Introduction & Scope",
    "Chapter 3 · Business Structure (28+ sections)",
    "Chapter 4 · Process Flows",
    "Chapter 5 · Reference Documents",
    "Chapter 6 · Gap Analysis & Recommendations",
    "Chapter 9 · Assumptions & Dependencies",
    "Chapter 10 · Sign Off Sheet",
  ];

  return (
    <div style={{ padding: "32px 36px" }}>
      <SectionTitle>Generate Solution Design Document</SectionTitle>

      <InfoBox title="🤖 AI-Powered SDD Generation">
        The AI analyses all questionnaire responses and produces a professional SDD matching
        industry-standard Oracle implementation templates — covering enterprise structure,
        process flows, gap analysis, and assumptions. Typical manual effort: 80–120 hours.
      </InfoBox>

      {analysis && (
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 28 }}>
          <StatCard value={analysis.answered_questions} label="Responses Loaded" />
          <StatCard value={analysis.modules?.length} label="Modules" />
          <StatCard value={`${analysis.completion_rate}%`} label="Completion Rate" accent="#F47920" />
        </div>
      )}

      <Card style={{ marginBottom: 24 }}>
        <div style={{ fontWeight: 700, color: "#0A1628", fontSize: "0.95rem", marginBottom: 20 }}>
          Document Configuration
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <ConfigField label="Company Name *" value={config.company_name} onChange={set("company_name")} placeholder="Acme Corporation" />
          <ConfigField label="Project Name" value={config.project_name} onChange={set("project_name")} placeholder="Oracle Fusion HCM Implementation" />
          <ConfigField label="Document Reference" value={config.doc_reference} onChange={set("doc_reference")} placeholder="CLIENT_CoreHR_SDD_V1.0" />
          <ConfigField label="Author" value={config.author} onChange={set("author")} placeholder="Your name or team" />
          <ConfigField label="Version" value={config.version} onChange={set("version")} placeholder="1.0" />
          <ConfigField label="Confidentiality" value={config.confidentiality} onChange={set("confidentiality")} placeholder="Confidential" />
        </div>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <div style={{ fontWeight: 700, color: "#0A1628", fontSize: "0.95rem", marginBottom: 14 }}>
          AI-Generated Sections
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {sddSections.map((s) => (
            <div
              key={s}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "10px 14px",
                background: "#F0F7FC",
                borderRadius: 8,
                fontSize: "0.85rem",
                color: "#0A1628",
              }}
            >
              <div style={{ width: 18, height: 18, borderRadius: 4, background: "#00B4C8", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                <svg width="10" height="7" viewBox="0 0 10 7" fill="none">
                  <path d="M1 3.5L3.5 6L9 1" stroke="#0A1628" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              {s}
              <span style={{ marginLeft: "auto", fontSize: "0.68rem", background: "linear-gradient(90deg,#1A5FA8,#00B4C8)", color: "#fff", padding: "2px 10px", borderRadius: 20, fontWeight: 700 }}>
                🤖 AI
              </span>
            </div>
          ))}
        </div>
      </Card>

      {error && (
        <div style={{ background: "#FFF4F4", border: "1px solid #E53935", borderRadius: 8, padding: "12px 16px", color: "#E53935", fontSize: "0.85rem", marginBottom: 16 }}>
          {error}
        </div>
      )}

      {!generating && !summary && (
        <Button variant="accent" onClick={handleGenerate}>
          🚀 Generate Complete SDD
        </Button>
      )}

      {generating && (
        <Card style={{ marginTop: 8 }}>
          <div style={{ fontWeight: 700, color: "#0A1628", marginBottom: 14 }}>Generating SDD…</div>
          <ProgressBar value={progress} />
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 6 }}>
            <span style={{ fontSize: "0.8rem", color: "#4A6A90" }}>{stage}</span>
            <span style={{ fontSize: "0.8rem", color: "#00B4C8", fontWeight: 700 }}>{progress}%</span>
          </div>
          <div
            style={{
              maxHeight: 180,
              overflowY: "auto",
              background: "#0A1628",
              borderRadius: 8,
              padding: "12px 16px",
              marginTop: 16,
              fontFamily: "monospace",
              fontSize: "0.78rem",
            }}
          >
            {logs.map((l, i) => (
              <div key={i} style={{ color: "#00B4C8", marginBottom: 3 }}>
                {l}
              </div>
            ))}
          </div>
        </Card>
      )}

      {summary && (
        <Card style={{ marginTop: 8, animation: "fadeUp 0.4s ease" }}>
          <style>{`@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}`}</style>
          <div style={{ fontWeight: 700, color: "#27AE60", fontSize: "1.1rem", marginBottom: 16 }}>
            ✅ SDD Generated Successfully!
          </div>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 20 }}>
            <StatCard value={summary.estimated_pages ?? "~60"} label="Est. Pages" />
            <StatCard value={summary.section_count ?? "40+"} label="Sections" />
            <StatCard value={summary.process_flow_count ?? "15+"} label="Process Flows" />
          </div>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            <Button variant="accent" onClick={handleDownload}>
              📥 Download DOCX
            </Button>
            <Button variant="ghost" onClick={handleGenerate}>
              🔄 Regenerate
            </Button>
          </div>
          <div style={{ marginTop: 16, padding: "12px 16px", background: "#EFF6FF", borderRadius: 8, fontSize: "0.82rem", color: "#1A5FA8" }}>
            <strong>💡 Time saved:</strong> Manual SDD creation takes 80–120 hours. AI generation completed in seconds — a <strong>99%+ efficiency gain.</strong>
          </div>
        </Card>
      )}
    </div>
  );
}