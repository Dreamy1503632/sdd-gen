import React from "react";
import { SIDEBAR_BG, TABS } from "../lib/constants";

export default function Sidebar({ activeTab, onTabChange, sddUnlocked }) {
  return (
    <aside
      style={{
        width: 220,
        minHeight: "calc(100vh - 60px)",
        background: SIDEBAR_BG,
        padding: "28px 0",
        display: "flex",
        flexDirection: "column",
        gap: 4,
        flexShrink: 0,
      }}
    >
      <div
        style={{
          padding: "0 20px 20px",
          borderBottom: "1px solid rgba(255,255,255,0.2)",
          marginBottom: 12,
        }}
      >
        <div style={{ fontSize: "0.68rem", fontWeight: 700, color: "rgba(10,22,40,0.6)", letterSpacing: "0.1em", textTransform: "uppercase" }}>
          Workflow
        </div>
      </div>
      {TABS.map((tab, i) => {
        const locked = tab.id === "sdd" && !sddUnlocked;
        const active = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => !locked && onTabChange(tab.id)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "12px 20px",
              border: "none",
              borderRadius: "0 8px 8px 0",
              marginRight: 12,
              cursor: locked ? "not-allowed" : "pointer",
              background: active ? "#0A1628" : "transparent",
              color: active ? "#00B4C8" : locked ? "rgba(10,22,40,0.4)" : "#0A1628",
              fontWeight: active ? 700 : 600,
              fontSize: "0.85rem",
              transition: "all 0.15s ease",
              textAlign: "left",
              opacity: locked ? 0.5 : 1,
            }}
          >
            <span style={{ fontSize: "1rem", flexShrink: 0 }}>{tab.icon}</span>
            <div style={{ flex: 1 }}>
              <div style={{ lineHeight: 1.2 }}>{tab.label}</div>
              <div style={{ fontSize: "0.65rem", opacity: 0.6, marginTop: 2 }}>
                Step {i + 1}
              </div>
            </div>
            {active && (
              <div
                style={{
                  width: 6,
                  height: 6,
                  borderRadius: "50%",
                  background: "#00B4C8",
                  flexShrink: 0,
                }}
              />
            )}
          </button>
        );
      })}
    </aside>
  );
}