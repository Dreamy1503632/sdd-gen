import React from "react";
import { EffortBadge, Badge } from "./UI";

function GapCard({ item }) {
  const hasGap =
    item.gap &&
    item.gap !== "None" &&
    !item.gap.toLowerCase().includes("none -") &&
    !item.gap.toLowerCase().includes("delivered");

  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #C8E0EC",
        borderRadius: 12,
        padding: "20px 24px",
        display: "flex",
        flexDirection: "column",
        gap: 14,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
        <Badge color="#0A1628">{item.module}</Badge>
        <EffortBadge effort={item.effort} />
        {!hasGap && <Badge color="#27AE60">✓ Oracle Native</Badge>}
      </div>

      <div>
        <div style={{ fontSize: "0.72rem", fontWeight: 700, color: "#4A6A90", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 4 }}>
          Requirement
        </div>
        <div style={{ fontSize: "0.88rem", color: "#0A1628", lineHeight: 1.6 }}>{item.requirement}</div>
      </div>

      <div style={{ background: "#F0FDF4", borderLeft: "3px solid #27AE60", padding: "10px 14px", borderRadius: "0 8px 8px 0" }}>
        <div style={{ fontSize: "0.72rem", fontWeight: 700, color: "#27AE60", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 4 }}>
          ✅ Oracle Capability
        </div>
        <div style={{ fontSize: "0.85rem", color: "#0A1628", lineHeight: 1.6 }}>{item.oracle_capability}</div>
      </div>

      {hasGap && (
        <div style={{ background: "#FFF4F4", borderLeft: "3px solid #E53935", padding: "10px 14px", borderRadius: "0 8px 8px 0" }}>
          <div style={{ fontSize: "0.72rem", fontWeight: 700, color: "#E53935", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 4 }}>
            ⚠ Gap
          </div>
          <div style={{ fontSize: "0.85rem", color: "#0A1628", lineHeight: 1.6 }}>{item.gap}</div>
        </div>
      )}

      <div style={{ background: "#EFF6FF", borderLeft: "3px solid #1A5FA8", padding: "10px 14px", borderRadius: "0 8px 8px 0" }}>
        <div style={{ fontSize: "0.72rem", fontWeight: 700, color: "#1A5FA8", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 4 }}>
          💡 Solution
        </div>
        <div style={{ fontSize: "0.85rem", color: "#0A1628", lineHeight: 1.6 }}>{item.solution}</div>
      </div>
    </div>
  );
}

export default function GapAnalysis({ items }) {
  if (!items || items.length === 0) return null;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {items.map((item, i) => (
        <GapCard key={i} item={item} />
      ))}
    </div>
  );
}