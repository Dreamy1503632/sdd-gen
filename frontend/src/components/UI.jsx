import React from "react";

export function Badge({ children, color = "#00B4C8" }) {
  return (
    <span
      style={{
        background: color,
        color: "#fff",
        fontSize: "0.7rem",
        fontWeight: 700,
        padding: "2px 10px",
        borderRadius: 20,
        letterSpacing: "0.04em",
        textTransform: "uppercase",
      }}
    >
      {children}
    </span>
  );
}

export function Card({ children, style = {} }) {
  return (
    <div
      style={{
        background: "#F0F7FC",
        border: "1px solid #C8E0EC",
        borderRadius: 12,
        padding: "24px 28px",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

export function StatCard({ value, label, accent = "#00B4C8" }) {
  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #C8E0EC",
        borderRadius: 12,
        padding: "20px 24px",
        textAlign: "center",
        flex: 1,
        minWidth: 140,
      }}
    >
      <div style={{ fontSize: "2.4rem", fontWeight: 800, color: accent, lineHeight: 1 }}>
        {value}
      </div>
      <div style={{ fontSize: "0.78rem", color: "#4A6A90", marginTop: 6, fontWeight: 600 }}>
        {label}
      </div>
    </div>
  );
}

export function Button({ children, onClick, variant = "primary", disabled = false, style = {} }) {
  const base = {
    border: "none",
    borderRadius: 10,
    padding: "12px 28px",
    fontWeight: 700,
    fontSize: "0.9rem",
    cursor: disabled ? "not-allowed" : "pointer",
    opacity: disabled ? 0.5 : 1,
    transition: "all 0.18s ease",
    display: "inline-flex",
    alignItems: "center",
    gap: 8,
    letterSpacing: "0.02em",
    ...style,
  };
  const variants = {
    primary: { background: "#0A1628", color: "#00B4C8" },
    accent:  { background: "#00B4C8", color: "#0A1628" },
    ghost:   { background: "transparent", color: "#0A1628", border: "2px solid #C8E0EC" },
    danger:  { background: "#F47920", color: "#fff" },
  };
  return (
    <button style={{ ...base, ...variants[variant] }} onClick={disabled ? undefined : onClick}>
      {children}
    </button>
  );
}

export function ProgressBar({ value, max = 100, color = "#00B4C8" }) {
  const pct = Math.round((value / max) * 100);
  return (
    <div style={{ background: "#C8E0EC", borderRadius: 99, height: 8, overflow: "hidden" }}>
      <div
        style={{
          height: "100%",
          width: `${pct}%`,
          background: color,
          borderRadius: 99,
          transition: "width 0.4s ease",
        }}
      />
    </div>
  );
}

export function SectionTitle({ children }) {
  return (
    <div style={{ marginBottom: 28 }}>
      <h2
        style={{
          fontSize: "1.6rem",
          fontWeight: 800,
          color: "#0A1628",
          margin: 0,
          paddingBottom: 14,
          borderBottom: "3px solid #00B4C8",
          display: "inline-block",
        }}
      >
        {children}
      </h2>
    </div>
  );
}

export function InfoBox({ title, children }) {
  return (
    <div
      style={{
        background: "#F0F7FC",
        borderLeft: "4px solid #00B4C8",
        borderRadius: "0 10px 10px 0",
        padding: "18px 22px",
        marginBottom: 28,
      }}
    >
      {title && (
        <div style={{ fontWeight: 700, color: "#0A1628", marginBottom: 6, fontSize: "0.95rem" }}>
          {title}
        </div>
      )}
      <div style={{ color: "#4A6A90", fontSize: "0.88rem", lineHeight: 1.7 }}>{children}</div>
    </div>
  );
}

export function LoadingOverlay({ message, progress }) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(10,22,40,0.93)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 9999,
        gap: 20,
      }}
    >
      <div
        style={{
          width: 56,
          height: 56,
          borderRadius: "50%",
          border: "5px solid rgba(0,180,200,0.2)",
          borderTop: "5px solid #00B4C8",
          animation: "spin 0.8s linear infinite",
        }}
      />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
      <div style={{ color: "#00B4C8", fontSize: "1rem", fontWeight: 700 }}>{message}</div>
      {progress !== undefined && (
        <div style={{ width: 320 }}>
          <ProgressBar value={progress} />
          <div style={{ color: "#4A6A90", fontSize: "0.8rem", textAlign: "center", marginTop: 6 }}>
            {progress}%
          </div>
        </div>
      )}
    </div>
  );
}

export function RiskBadge({ severity }) {
  const map = {
    Low:      "#27AE60",
    Medium:   "#F47920",
    High:     "#E53935",
    Critical: "#B71C1C",
  };
  return (
    <span
      style={{
        background: map[severity] || "#4A6A90",
        color: "#fff",
        fontSize: "0.7rem",
        fontWeight: 700,
        padding: "2px 10px",
        borderRadius: 20,
      }}
    >
      {severity}
    </span>
  );
}

export function EffortBadge({ effort }) {
  const map = { Low: "#27AE60", Medium: "#F47920", High: "#E53935" };
  return (
    <span
      style={{
        background: map[effort] || "#4A6A90",
        color: "#fff",
        fontSize: "0.7rem",
        fontWeight: 700,
        padding: "2px 10px",
        borderRadius: 20,
      }}
    >
      {effort}
    </span>
  );
}