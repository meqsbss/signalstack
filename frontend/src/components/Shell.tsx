import type { CSSProperties } from "react";
import { NavLink, Outlet } from "react-router-dom";

const linkStyle = ({ isActive }: { isActive: boolean }): CSSProperties => ({
  display: "flex",
  alignItems: "center",
  height: 40,
  padding: "0 16px",
  color: isActive ? "var(--text)" : "var(--text-muted)",
  background: isActive ? "var(--surface-raised)" : "transparent",
  borderLeft: isActive ? "2px solid var(--accent)" : "2px solid transparent",
  fontSize: 14,
  textDecoration: "none",
});

export default function Shell() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: 240,
          flexShrink: 0,
          background: "var(--surface)",
          borderRight: "1px solid var(--border)",
          padding: "16px 0",
        }}
      >
        <div
          style={{
            padding: "0 16px 16px",
            fontSize: 16,
            fontWeight: 600,
            letterSpacing: "0.02em",
          }}
        >
          SignalStack
        </div>
        <nav>
          <NavLink to="/" end style={linkStyle}>
            Competitors
          </NavLink>
          <NavLink to="/briefing" style={linkStyle}>
            Briefing
          </NavLink>
        </nav>
      </aside>

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <header
          style={{
            height: 56,
            display: "flex",
            alignItems: "center",
            padding: "0 24px",
            borderBottom: "1px solid var(--border)",
            background: "var(--bg)",
          }}
        >
          <h1 style={{ fontSize: 24 }}>SignalStack</h1>
        </header>

        <main
          style={{
            flex: 1,
            maxWidth: 1100,
            width: "100%",
            margin: "0 auto",
            padding: 24,
          }}
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}