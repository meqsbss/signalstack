import { useAsync } from "../hooks/useAsync";
import { getSignalService } from "../services/provider";
import { useToast } from "../hooks/useToast";
import EmptyState from "../components/EmptyState";
import SkeletonRows from "../components/SkeletonRows";
import SeverityBadge from "../components/SeverityBadge";
import { relativeTime } from "../utils/format";

export default function BriefingPage() {
  const svc = getSignalService();
  const { push } = useToast();
  const { data, loading, error, reload } = useAsync(() => svc.getLatestBriefing(), []);

  async function onGenerate() {
    try {
      await svc.generateBriefing();
      push("Briefing generated", "success");
      reload();
    } catch {
      push("Could not generate briefing", "error");
    }
  }

  if (loading) return <SkeletonRows rows={4} />;
  if (error) return <EmptyState message="Could not load briefing." action={<button onClick={reload} style={primaryBtn}>Retry</button>} />;

  if (!data)
    return (
      <EmptyState
        message="No briefing yet."
        action={<button onClick={onGenerate} style={primaryBtn}>Generate briefing</button>}
      />
    );

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
        <h2>Briefing — week of {data.week_start.slice(0, 10)}</h2>
        <button onClick={onGenerate} style={secondaryBtn}>Regenerate</button>
      </div>
      <p style={{ color: "var(--text-muted)", marginBottom: 24 }}>{data.summary_text}</p>
      {data.top_events.map((e) => (
        <div key={e.id} style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 0", borderBottom: "1px solid var(--border)" }}>
          <SeverityBadge severity={e.severity} />
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-muted)" }}>{e.competitor_name}</span>
          <span style={{ flex: 1 }}>{e.diff_summary}</span>
          <span style={{ color: "var(--text-muted)", fontSize: 12 }}>{relativeTime(e.detected_at)}</span>
        </div>
      ))}
    </div>
  );
}

const primaryBtn = { background: "var(--accent)", color: "white", border: "none", padding: "8px 16px", borderRadius: "var(--radius-card)", cursor: "pointer" };
const secondaryBtn = { background: "transparent", border: "1px solid var(--border)", color: "var(--text)", padding: "8px 16px", borderRadius: "var(--radius-card)", cursor: "pointer" };