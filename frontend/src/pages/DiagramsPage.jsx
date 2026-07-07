import React, { useState } from "react";
import { CHART_COLORS } from "../lib/constants";
import { SectionTitle, InfoBox, Button, Card } from "../components/UI";

const DIAGRAM_TYPES = [
  { id: "architecture", label: "System Architecture", icon: "🏢" },
  { id: "integration", label: "Integration Landscape", icon: "🔗" },
  { id: "dataflow", label: "Employee Data Flow", icon: "📊" },
  { id: "roadmap", label: "Implementation Roadmap", icon: "📅" },
];

function ArchitectureSVG({ modules }) {
  const coreModules = modules ?? [
    "Core HR","Talent Management","Payroll","Workforce Management",
  ];
  const cols = Math.ceil(coreModules.length / 2);
  return (
    <svg viewBox="0 0 800 460" xmlns="http://www.w3.org/2000/svg" style={{ width: "100%", borderRadius: 12 }}>
      <rect width="800" height="460" fill="#F0F7FC" rx="12" />
      <rect x="20" y="20" width="760" height="60" rx="10" fill="#0A1628" />
      <text x="400" y="56" textAnchor="middle" fill="#00B4C8" fontSize="18" fontWeight="800" fontFamily="sans-serif">
        Oracle Fusion HCM Cloud
      </text>
      {coreModules.map((m, i) => {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = 40 + col * (720 / cols);
        const y = 110 + row * 120;
        const w = 720 / cols - 20;
        return (
          <g key={m}>
            <rect x={x} y={y} width={w} height={80} rx="8" fill="#fff" stroke={CHART_COLORS[i % CHART_COLORS.length]} strokeWidth="2" />
            <rect x={x} y={y} width={w} height={8} rx="4" fill={CHART_COLORS[i % CHART_COLORS.length]} />
            <text x={x + w / 2} y={y + 50} textAnchor="middle" fill="#0A1628" fontSize="12" fontWeight="700" fontFamily="sans-serif">
              {m}
            </text>
          </g>
        );
      })}
      <rect x="20" y="380" width="240" height="60" rx="8" fill="#fff" stroke="#C8E0EC" strokeWidth="2" />
      <text x="140" y="415" textAnchor="middle" fill="#4A6A90" fontSize="11" fontFamily="sans-serif">ERP / Finance</text>
      <rect x="280" y="380" width="240" height="60" rx="8" fill="#fff" stroke="#C8E0EC" strokeWidth="2" />
      <text x="400" y="415" textAnchor="middle" fill="#4A6A90" fontSize="11" fontFamily="sans-serif">Payroll / Benefits Vendors</text>
      <rect x="540" y="380" width="240" height="60" rx="8" fill="#fff" stroke="#C8E0EC" strokeWidth="2" />
      <text x="660" y="415" textAnchor="middle" fill="#4A6A90" fontSize="11" fontFamily="sans-serif">Identity / SSO</text>
    </svg>
  );
}

function RoadmapSVG({ modules }) {
  const phases = [
    { label: "Phase 1", duration: "Months 1–4", color: "#0A1628", mods: (modules ?? []).slice(0, 2) },
    { label: "Phase 2", duration: "Months 4–8", color: "#1A5FA8", mods: (modules ?? []).slice(2, 5) },
    { label: "Phase 3", duration: "Months 8–12", color: "#00B4C8", mods: (modules ?? []).slice(5) },
  ];
  return (
    <svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg" style={{ width: "100%", borderRadius: 12 }}>
      <rect width="800" height="280" fill="#F0F7FC" rx="12" />
      {phases.map((p, i) => {
        const x = 20 + i * 260;
        return (
          <g key={p.label}>
            <rect x={x} y={20} width={240} height={240} rx="10" fill="#fff" stroke={p.color} strokeWidth="2" />
            <rect x={x} y={20} width={240} height={40} rx="8" fill={p.color} />
            <text x={x + 120} y={44} textAnchor="middle" fill="#fff" fontSize="13" fontWeight="800" fontFamily="sans-serif">
              {p.label}
            </text>
            <text x={x + 120} y={78} textAnchor="middle" fill="#4A6A90" fontSize="11" fontFamily="sans-serif">
              {p.duration}
            </text>
            {p.mods.map((m, j) => (
              <g key={m}>
                <rect x={x + 16} y={94 + j * 44} width={208} height={36} rx="6" fill={p.color + "18"} stroke={p.color + "44"} strokeWidth="1" />
                <text x={x + 120} y={116 + j * 44} textAnchor="middle" fill="#0A1628" fontSize="11" fontWeight="600" fontFamily="sans-serif">
                  {m}
                </text>
              </g>
            ))}
          </g>
        );
      })}
    </svg>
  );
}

export default function DiagramsPage({ analysis }) {
  const [selected, setSelected] = useState("architecture");
  const modules = analysis?.modules;

  const renderDiagram = () => {
    if (selected === "architecture") return <ArchitectureSVG modules={modules} />;
    if (selected === "roadmap") return <RoadmapSVG modules={modules} />;
    return (
      <div
        style={{
          height: 300,
          background: "#F0F7FC",
          borderRadius: 12,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          color: "#4A6A90",
          gap: 10,
        }}
      >
        <div style={{ fontSize: "3rem" }}>🎨</div>
        <div style={{ fontWeight: 700, fontSize: "1rem", color: "#0A1628" }}>
          {DIAGRAM_TYPES.find((d) => d.id === selected)?.label}
        </div>
        <div style={{ fontSize: "0.85rem" }}>
          Connect the backend and upload a questionnaire to generate this diagram.
        </div>
      </div>
    );
  };

  return (
    <div style={{ padding: "32px 36px" }}>
      <SectionTitle>Architecture Diagrams</SectionTitle>

      <InfoBox title="🏗️ Visual Architecture">
        Generate professional diagrams for executive presentations. Each diagram is derived from your
        analysis results and covers the Oracle HCM solution components, integrations, and roadmap.
      </InfoBox>

      {!analysis && (
        <div
          style={{
            padding: "48px 0",
            textAlign: "center",
            color: "#4A6A90",
          }}
        >
          <div style={{ fontSize: "3rem", marginBottom: 12 }}>📊</div>
          <div style={{ fontWeight: 700, color: "#0A1628", marginBottom: 8 }}>No analysis data</div>
          <div style={{ fontSize: "0.88rem" }}>
            Please upload and analyse a questionnaire first.
          </div>
        </div>
      )}

      {analysis && (
        <>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 24 }}>
            {DIAGRAM_TYPES.map((d) => (
              <button
                key={d.id}
                onClick={() => setSelected(d.id)}
                style={{
                  padding: "10px 18px",
                  borderRadius: 8,
                  border: `2px solid ${selected === d.id ? "#00B4C8" : "#C8E0EC"}`,
                  background: selected === d.id ? "rgba(0,180,200,0.1)" : "#fff",
                  color: selected === d.id ? "#0A1628" : "#4A6A90",
                  fontWeight: selected === d.id ? 700 : 500,
                  fontSize: "0.85rem",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  transition: "all 0.15s ease",
                }}
              >
                {d.icon} {d.label}
              </button>
            ))}
          </div>

          <Card style={{ marginBottom: 20, padding: 24 }}>
            {renderDiagram()}
          </Card>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            <Button variant="accent" onClick={() => alert("Export SVG — connect backend to enable")}>
              ⬇ Export SVG
            </Button>
            <Button variant="ghost" onClick={() => alert("Export PNG — connect backend to enable")}>
              🖼 Export PNG
            </Button>
          </div>
        </>
      )}
    </div>
  );
}