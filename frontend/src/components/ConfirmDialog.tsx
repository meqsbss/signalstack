import type { ReactNode } from "react";

export default function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = "Confirm",
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  message: ReactNode;
  confirmLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  if (!open) return null;
  return (
    <div
      role="dialog"
      aria-modal="true"
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          background: "var(--surface)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius-card)",
          padding: 24,
          maxWidth: 400,
          width: "90%",
        }}
      >
        <h2 style={{ marginBottom: 12 }}>{title}</h2>
        <div style={{ marginBottom: 24, color: "var(--text-muted)" }}>{message}</div>
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onCancel} style={secondaryBtn}>Cancel</button>
          <button onClick={onConfirm} style={dangerBtn}>{confirmLabel}</button>
        </div>
      </div>
    </div>
  );
}

const secondaryBtn = {
  background: "transparent",
  border: "1px solid var(--border)",
  color: "var(--text)",
  padding: "8px 16px",
  borderRadius: "var(--radius-card)",
} as const;

const dangerBtn = {
  background: "var(--danger)",
  border: "none",
  color: "white",
  padding: "8px 16px",
  borderRadius: "var(--radius-card)",
} as const;