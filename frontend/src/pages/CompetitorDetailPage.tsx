import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAsync } from "../hooks/useAsync";
import { getSignalService } from "../services/provider";
import { useToast } from "../hooks/useToast";
import EmptyState from "../components/EmptyState";
import SkeletonRows from "../components/SkeletonRows";
import SeverityBadge from "../components/SeverityBadge";
import DiffViewer from "../components/DiffViewer";
import ConfirmDialog from "../components/ConfirmDialog";
import { formatCurrency, formatNumber, formatPercent, relativeTime } from "../utils/format";

type Tab = "changes" | "revenue" | "briefing";

export default function CompetitorDetailPage() {
  const { id = "" } = useParams();
  const svc = getSignalService();
  const navigate = useNavigate();
  const { push } = useToast();
  const [tab, setTab] = useState<Tab>("changes");
  const [refreshing, setRefreshing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [expanded, setExpanded] = useState<string | null>(null);

  const competitor = useAsync(() => svc.getCompetitor(id), [id]);
  const events = useAsync(() => svc.listChangeEvents(id), [id]);
  const revenue = useAsync(() => svc.getRevenueContext(id), [id]);

  if (competitor.loading) return <SkeletonRows rows={3} />;
  if (competitor.error)
    return <EmptyState message="Competitor not found." action={<button onClick={() => navigate("/")} style={linkBtn}>Back</button>} />;

  const c = competitor.data!;

  async function onRefresh() {
    setRefreshing(true);
    try {
      await svc.refreshCompetitor(id);
      push("Refreshed", "success");
      events.reload();
      competitor.reload();
    } catch {
      push("Refresh failed", "error");
    } finally {
      setRefreshing(false);
    }
  }

  async function onDelete() {
    await svc.deleteCompetitor(id);
    push("Deleted", "success");
    navigate("/");
  }

  async function onAcknowledge(eventId: string) {
    try {
      await svc.acknowledgeChangeEvent(eventId);
      events.reload();
    } catch {
      push("Could not acknowledge", "error");
    }
  }

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 24 }}>
        <h2>{c.name}</h2>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 13, color: "var(--text-muted)" }}>{c.domain}</span>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          <button onClick={onRefresh} disabled={refreshing} style={primaryBtn}>
            {refreshing ? "Refreshing..." : "Refresh now"}
          </button>
          <button onClick={() => setConfirmDelete(true)} style={dangerBtn}>Delete</button>
        </div>
      </div>

      <div style={{ display: "flex", gap: 0, borderBottom: "1px solid var(--border)", marginBottom: 16 }}>
        {(["changes", "revenue", "briefing"] as Tab[]).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              background: "transparent",
              border: "none",
              borderBottom: tab === t ? "2px solid var(--accent)" : "2px solid transparent",
              color: tab === t ? "var(--text)" : "var(--text-muted)",
              padding: "8px 16px",
              cursor: "pointer",
              textTransform: "capitalize",
            }}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "changes" && (
        <div>
          {events.loading && <SkeletonRows rows={3} />}
          {!events.loading && events.data && events.data.length === 0 && (
            <EmptyState message="No changes detected yet. Refresh to check." />
          )}
          {events.data?.map((e) => (
            <div key={e.id} style={{ borderBottom: "1px solid var(--border)", padding: "12px 0", opacity: e.acknowledged ? 0.5 : 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <SeverityBadge severity={e.severity} />
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-muted)" }}>{e.source_type}</span>
                <span
                  onClick={() => setExpanded(expanded === e.id ? null : e.id)}
                  style={{ cursor: "pointer", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
                >
                  {e.diff_summary}
                </span>
                <span style={{ color: "var(--text-muted)", fontSize: 12 }}>{relativeTime(e.detected_at)}</span>
                {!e.acknowledged && (
                  <button onClick={() => onAcknowledge(e.id)} style={secondaryBtn}>Acknowledge</button>
                )}
              </div>
              {expanded === e.id && <DiffViewer diff={e.diff_full} />}
            </div>
          ))}
        </div>
      )}

      {tab === "revenue" && (
        <div>
          {revenue.loading && <SkeletonRows rows={2} />}
          {!revenue.loading && revenue.data === null && (
            <EmptyState message="No verified revenue data." />
          )}
          {revenue.data && (
            <div style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: "var(--radius-card)", padding: 16 }}>
              <div style={{ display: "flex", gap: 32 }}>
                <div>
                  <div style={statLabel}>MRR</div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 20 }}>{formatCurrency(revenue.data.mrr)}</div>
                </div>
                <div>
                  <div style={statLabel}>30d growth</div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 20, color: revenue.data.growth_30d >= 0 ? "var(--success)" : "var(--danger)" }}>
                    {formatPercent(revenue.data.growth_30d)}
                  </div>
                </div>
              </div>
              <div style={{ marginTop: 12, fontSize: 12, color: "var(--success)" }}>
                Verified via TrustMRR ({formatNumber(revenue.data.mrr)} MRR)
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "briefing" && <p style={{ color: "var(--text-muted)" }}>See the Briefing page for the latest weekly digest.</p>}

      <ConfirmDialog
        open={confirmDelete}
        title={`Delete ${c.name}?`}
        message="This removes all snapshots and change events for this competitor."
        confirmLabel="Delete"
        onConfirm={onDelete}
        onCancel={() => setConfirmDelete(false)}
      />
    </div>
  );
}

const statLabel = { fontSize: 12, textTransform: "uppercase" as const, letterSpacing: "0.04em", color: "var(--text-muted)", marginBottom: 4 };
const primaryBtn = { background: "var(--accent)", color: "white", border: "none", padding: "8px 16px", borderRadius: "var(--radius-card)", cursor: "pointer" };
const secondaryBtn = { background: "transparent", border: "1px solid var(--border)", color: "var(--text)", padding: "4px 12px", borderRadius: "var(--radius-card)", cursor: "pointer", fontSize: 12 };
const dangerBtn = { background: "var(--danger)", color: "white", border: "none", padding: "8px 16px", borderRadius: "var(--radius-card)", cursor: "pointer" };
const linkBtn = { background: "transparent", border: "none", color: "var(--accent)", cursor: "pointer", fontSize: 14 };