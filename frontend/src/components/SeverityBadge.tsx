import type { Severity } from "../types";

const colors: Record<Severity, { color: string; border: string; bg: string }> = {
  low: { color: "var(--severity-low)", border: "var(--severity-low)", bg: "transparent" },
  medium: { color: "var(--severity-medium)", border: "var(--severity-medium)", bg: "transparent" },
  high: { color: "white", border: "var(--severity-high)", bg: "var(--severity-high)" },
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  const c = colors[severity];
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 8px",
        borderRadius: "var(--radius-badge)",
        fontSize: 12,
        fontWeight: 500,
        textTransform: "uppercase",
        color: c.color,
        border: `1px solid ${c.border}`,
        background: c.bg,
      }}
    >
      {severity}
    </span>
  );
}