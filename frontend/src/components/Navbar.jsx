import React from "react";
import { NAV_BG } from "../lib/constants";

export default function Navbar() {
  return (
    <header
      style={{
        background: NAV_BG,
        padding: "0 32px",
        height: 60,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        position: "sticky",
        top: 0,
        zIndex: 100,
        borderBottom: "1px solid rgba(0,180,200,0.2)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <div
          style={{
            width: 34,
            height: 34,
            borderRadius: 8,
            background: "linear-gradient(135deg,#00B4C8,#0AD4E8)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 900,
            fontSize: "1rem",
            color: "#0A1628",
          }}
        >
          O
        </div>
        <div>
          <span
            style={{
              fontWeight: 800,
              fontSize: "0.95rem",
              color: "#fff",
              letterSpacing: "-0.01em",
            }}
          >
            Oracle Fusion
          </span>
          <span style={{ color: "#00B4C8", fontWeight: 800, fontSize: "0.95rem" }}> HCM</span>
          <span style={{ color: "#4A6A90", fontWeight: 400, fontSize: "0.8rem", marginLeft: 8 }}>
            Solution Architect
          </span>
        </div>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span
          style={{
            background: "rgba(0,180,200,0.15)",
            border: "1px solid rgba(0,180,200,0.3)",
            color: "#00B4C8",
            fontSize: "0.72rem",
            fontWeight: 700,
            padding: "4px 12px",
            borderRadius: 20,
            letterSpacing: "0.06em",
          }}
        >
          AI-POWERED · v2.0
        </span>
      </div>
    </header>
  );
}