import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div style={{ textAlign: "center", marginTop: 48 }}>
      <p style={{ color: "var(--text-muted)" }}>Page not found.</p>
      <Link to="/">Back to competitors</Link>
    </div>
  );
}