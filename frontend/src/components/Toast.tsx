import { useToast } from "../hooks/useToast";

export default function ToastContainer() {
  const { toasts } = useToast();
  return (
    <div style={{ position: "fixed", bottom: 24, right: 24, display: "flex", flexDirection: "column", gap: 8 }}>
      {toasts.map((t) => (
        <div
          key={t.id}
          role="status"
          style={{
            background: "var(--surface-raised)",
            border: "1px solid var(--border)",
            borderLeft: `3px solid ${t.kind === "success" ? "var(--success)" : "var(--danger)"}`,
            borderRadius: "var(--radius-card)",
            padding: "12px 16px",
            minWidth: 240,
          }}
        >
          {t.message}
        </div>
      ))}
    </div>
  );
}