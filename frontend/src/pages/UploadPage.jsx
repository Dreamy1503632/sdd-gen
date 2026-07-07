import React, { useState, useRef } from "react";
import { uploadAndAnalyze } from "../lib/api";
import GapAnalysis from "../components/GapAnalysis";
import {
  Button, SectionTitle, InfoBox, StatCard, Card,
  LoadingOverlay, RiskBadge,
} from "../components/UI";

function Section({ title, children }) {
  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #C8E0EC",
        borderRadius: 12,
        padding: "22px 26px",
        marginBottom: 16,
      }}
    >
      <div style={{ fontWeight: 700, color: "#0A1628", fontSize: "0.95rem", marginBottom: 14 }}>
        {title}
      </div>
      {children}
    </div>
  );
}

function BulletList({ items }) {
  return (
    <ul style={{ margin: 0, paddingLeft: 20 }}>
      {items.map((item, i) => (
        <li key={i} style={{ color: "#4A6A90", fontSize: "0.87rem", lineHeight: 1.7, marginBottom: 4 }}>
          {item}
        </li>
      ))}
    </ul>
  );
}

export default function UploadPage({ onAnalysisDone }) {
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [loadMsg, setLoadMsg] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const inputRef = useRef();

  const fakeProgress = () => {
    const steps = [
      [10, "Reading Excel file…"],
      [25, "Parsing questionnaire responses…"],
      [45, "Connecting to AI…"],
      [65, "Analysing requirements…"],
      [80, "Building gap analysis…"],
      [92, "Generating recommendations…"],
    ];
    let i = 0;
    const iv = setInterval(() => {
      if (i >= steps.length) { clearInterval(iv); return; }
      setProgress(steps[i][0]);
      setLoadMsg(steps[i][1]);
      i++;
    }, 700);
    return iv;
  };

  const handleFile = async (file) => {
    if (!file) return;
    setError(null);
    setLoading(true);
    setProgress(0);
    const iv = fakeProgress();
    try {
      const result = await uploadAndAnalyze(file);
      clearInterval(iv);
      setProgress(100);
      setLoadMsg("Analysis complete!");
      setTimeout(() => {
        setLoading(false);
        setAnalysis(result);
        onAnalysisDone && onAnalysisDone(result);
      }, 600);
    } catch (e) {
      clearInterval(iv);
      setLoading(false);
      setError(e.message);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const cp = analysis?.company_profile || {};
  const tl = analysis?.timeline || {};

  return (
    <div style={{ padding: "32px 36px", maxWidth: 960 }}>
      {loading && <LoadingOverlay message={loadMsg} progress={progress} />}
      <SectionTitle>Upload & AI Analysis</SectionTitle>

      <InfoBox title="🤖 AI-Powered Requirement Analysis">
        Upload the completed Excel questionnaire. The AI extracts key findings, identifies gaps
        against Oracle Fusion HCM capabilities, and generates prioritised recommendations.
      </InfoBox>

      {!analysis && (
        <div
          onDrop={onDrop}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onClick={() => inputRef.current?.click()}
          style={{
            border: `2px dashed ${dragging ? "#00B4C8" : "#C8E0EC"}`,
            borderRadius: 16,
            padding: "60px 40px",
            textAlign: "center",
            cursor: "pointer",
            background: dragging ? "rgba(0,180,200,0.05)" : "#FAFCFE",
            transition: "all 0.2s ease",
            marginBottom: 24,
          }}
        >
          <div style={{ fontSize: "3.2rem", marginBottom: 12 }}>📤</div>
          <div style={{ fontWeight: 700, color: "#0A1628", fontSize: "1rem", marginBottom: 6 }}>
            Drop your Excel questionnaire here
          </div>
          <div style={{ color: "#4A6A90", fontSize: "0.85rem" }}>or click to browse · .xlsx / .xls</div>
          <input
            ref={inputRef}
            type="file"
            accept=".xlsx,.xls"
            style={{ display: "none" }}
            onChange={(e) => handleFile(e.target.files[0])}
          />
        </div>
      )}

      {error && (
        <div style={{ background: "#FFF4F4", border: "1px solid #E53935", borderRadius: 8, padding: "12px 16px", color: "#E53935", fontSize: "0.85rem", marginBottom: 16 }}>
          {error}
        </div>
      )}

      {analysis && (
        <div style={{ animation: "fadeUp 0.4s ease" }}>
          <style>{`@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}`}</style>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 24 }}>
            <StatCard value={analysis.answered_questions ?? "—"} label="Answered Questions" />
            <StatCard value={analysis.total_questions ?? "—"} label="Total Questions" />
            <StatCard value={`${analysis.completion_rate ?? "—"}%`} label="Completion Rate" accent="#F47920" />
            <StatCard value={analysis.modules?.length ?? "—"} label="Modules" />
          </div>

          <Section title="🏢 Company Profile">
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 8 }}>
              {[
                ["Industry", analysis.industry],
                ["Employee Count", cp.employee_count],
                ["Locations", cp.locations],
                ["Countries", cp.countries],
                ["Complexity", cp.key_complexity],
              ].map(([k, v]) =>
                v ? (
                  <div key={k} style={{ fontSize: "0.85rem" }}>
                    <span style={{ fontWeight: 700, color: "#0A1628" }}>{k}: </span>
                    <span style={{ color: "#4A6A90" }}>{v}</span>
                  </div>
                ) : null
              )}
            </div>
          </Section>

          <Section title="🔍 Key Findings">
            <BulletList items={analysis.key_findings ?? []} />
          </Section>

          <Section title="⚠️ Pain Points">
            <BulletList items={analysis.pain_points ?? []} />
          </Section>

          <Section title="📋 Requirements">
            <BulletList items={analysis.requirements ?? []} />
          </Section>

          <Section title="🔄 Gap Analysis">
            <GapAnalysis items={analysis.gap_analysis ?? []} />
          </Section>

          <Section title="💡 Recommendations">
            <BulletList items={analysis.recommendations ?? []} />
          </Section>

          <Section title="⚡ Risk Assessment">
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {(analysis.risks ?? []).map((r, i) => (
                <div
                  key={i}
                  style={{ display: "flex", gap: 14, alignItems: "flex-start", borderLeft: "3px solid #F47920", paddingLeft: 14 }}
                >
                  <div style={{ flex: 1 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                      <span style={{ fontWeight: 700, fontSize: "0.88rem", color: "#0A1628" }}>{r.risk}</span>
                      <RiskBadge severity={r.severity} />
                    </div>
                    <div style={{ fontSize: "0.82rem", color: "#4A6A90" }}>
                      <em>Mitigation:</em> {r.mitigation}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Section>

          <Section title="📅 Implementation Timeline">
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 8 }}>
              {[
                ["Phase 1", tl.phase1],
                ["Phase 2", tl.phase2],
                ["Phase 3", tl.phase3],
                ["Total", tl.total_duration],
                ["Critical Path", tl.critical_path],
              ].map(([k, v]) =>
                v && v !== "N/A" ? (
                  <div key={k} style={{ fontSize: "0.85rem" }}>
                    <span style={{ fontWeight: 700, color: "#0A1628" }}>{k}: </span>
                    <span style={{ color: "#4A6A90" }}>{v}</span>
                  </div>
                ) : null
              )}
            </div>
          </Section>

          <div style={{ display: "flex", gap: 12, marginTop: 8, flexWrap: "wrap" }}>
            <Button
              variant="ghost"
              onClick={() => { setAnalysis(null); onAnalysisDone && onAnalysisDone(null); }}
            >
              ↩ Upload Another
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}