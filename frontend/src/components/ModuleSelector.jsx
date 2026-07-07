import React from "react";
import { HCM_MODULES } from "../lib/constants";

export default function ModuleSelector({ selected, onChange }) {
  const toggle = (m) =>
    onChange(selected.includes(m) ? selected.filter((x) => x !== m) : [...selected, m]);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
        gap: 12,
      }}
    >
      {HCM_MODULES.map((m) => {
        const on = selected.includes(m);
        return (
          <label
            key={m}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "14px 18px",
              borderRadius: 10,
              border: `2px solid ${on ? "#00B4C8" : "#C8E0EC"}`,
              background: on ? "rgba(0,180,200,0.07)" : "#fff",
              cursor: "pointer",
              transition: "all 0.15s ease",
              userSelect: "none",
            }}
          >
            <div
              style={{
                width: 20,
                height: 20,
                borderRadius: 5,
                border: `2px solid ${on ? "#00B4C8" : "#C8E0EC"}`,
                background: on ? "#00B4C8" : "transparent",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
                transition: "all 0.15s ease",
              }}
            >
              {on && (
                <svg width="11" height="8" viewBox="0 0 11 8" fill="none">
                  <path d="M1 4L4 7L10 1" stroke="#0A1628" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
            </div>
            <input
              type="checkbox"
              checked={on}
              onChange={() => toggle(m)}
              style={{ display: "none" }}
            />
            <span
              style={{
                fontSize: "0.85rem",
                fontWeight: on ? 700 : 500,
                color: on ? "#0A1628" : "#4A6A90",
              }}
            >
              {m}
            </span>
          </label>
        );
      })}
    </div>
  );
}