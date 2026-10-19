import { Link, useNavigate } from "react-router-dom";
import { useAsync } from "../hooks/useAsync";
import { getSignalService } from "../services/provider";
import EmptyState from "../components/EmptyState";
import SkeletonRows from "../components/SkeletonRows";
import { relativeTime } from "../utils/format";

export default function CompetitorsPage() {
  const svc = getSignalService();
  const navigate = useNavigate();
  const { data, loading, error, reload } = useAsync(() => svc.listCompetitors(), []);

  if (loading) return <SkeletonRows rows={5} />;
  if (error)
    return (
      <EmptyState
        message="Could not load competitors."
        action={<button onClick={reload} style={primaryBtn}>Retry</button>}
      />
    );
  if (!data || data.length === 0)
    return (
      <EmptyState
        message="No competitors yet. Add your first competitor."
        action={<Link to="/add" style={{ ...primaryBtn, display: "inline-block", textDecoration: "none" }}>Add competitor</Link>}
      />
    );

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
        <h2>Competitors</h2>
        <Link to="/add" style={{ ...primaryBtn, textDecoration: "none" }}>Add competitor</Link>
      </div>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid var(--border)" }}>
            <th style={th}>Name</th>
            <th style={th}>Domain</th>
            <th style={th}>Last refreshed</th>
          </tr>
        </thead>
        <tbody>
          {data.map((c) => (
            <tr
              key={c.id}
              onClick={() => navigate(`/competitor/${c.id}`)}
              style={{ height: 40, borderBottom: "1px solid var(--border)", cursor: "pointer" }}
              onMouseEnter={(e) => (e.currentTarget.style.background = "var(--surface-raised)")}
              onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
            >
              <td style={td}>{c.name}</td>
              <td style={{ ...td, fontFamily: "var(--font-mono)", fontSize: 13 }}>{c.domain}</td>
              <td style={{ ...td, color: "var(--text-muted)" }}>{relativeTime(c.last_refreshed_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const th = {
  textAlign: "left" as const,
  padding: "8px 12px",
  fontSize: 12,
  fontWeight: 500,
  textTransform: "uppercase" as const,
  letterSpacing: "0.04em",
  color: "var(--text-muted)",
};
const td = { padding: "8px 12px" };
const primaryBtn = {
  background: "var(--accent)",
  color: "white",
  border: "none",
  padding: "8px 16px",
  borderRadius: "var(--radius-card)",
  cursor: "pointer",
  fontSize: 14,
};