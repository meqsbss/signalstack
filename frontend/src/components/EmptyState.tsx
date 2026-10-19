import { ReactNode } from "react";

export default function EmptyState({
  message,
  action,
}: {
  message: string;
  action?: ReactNode;
}) {
  return (
    <div style={{ textAlign: "center", padding: "48px 0", maxWidth: 360, margin: "0 auto" }}>
      <p style={{ color: "var(--text-muted)", marginBottom: 16 }}>{message}</p>
      {action}
    </div>
  );
}