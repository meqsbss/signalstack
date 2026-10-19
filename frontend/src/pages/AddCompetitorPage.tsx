import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getSignalService } from "../services/provider";
import { useToast } from "../hooks/useToast";
import { isValidDomain } from "../utils/validation";

export default function AddCompetitorPage() {
  const svc = getSignalService();
  const navigate = useNavigate();
  const { push } = useToast();
  const [name, setName] = useState("");
  const [domain, setDomain] = useState("");
  const [slug, setSlug] = useState("");
  const [domainError, setDomainError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const disabled = !name.trim() || !domain.trim() || submitting;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!isValidDomain(domain)) {
      setDomainError("Enter a valid domain, e.g. example.com");
      return;
    }
    setDomainError(null);
    setSubmitting(true);
    try {
      const c = await svc.addCompetitor({
        name: name.trim(),
        domain: domain.trim(),
        trustmrr_slug: slug.trim() || null,
      });
      push("Competitor added", "success");
      navigate(`/competitor/${c.id}`);
    } catch {
      push("Could not add competitor", "error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} style={{ maxWidth: 480 }}>
      <h2 style={{ marginBottom: 16 }}>Add competitor</h2>

      <label style={label}>Name</label>
      <input value={name} onChange={(e) => setName(e.target.value)} style={input} />

      <label style={label}>Domain</label>
      <input value={domain} onChange={(e) => setDomain(e.target.value)} style={input} />
      {domainError && <p style={{ color: "var(--danger)", fontSize: 12, margin: "4px 0" }}>{domainError}</p>}

      <label style={label}>TrustMRR slug (optional)</label>
      <input value={slug} onChange={(e) => setSlug(e.target.value)} style={input} />

      <div style={{ display: "flex", gap: 8, marginTop: 24 }}>
        <button type="submit" disabled={disabled} style={{ ...primaryBtn, opacity: disabled ? 0.4 : 1 }}>
          Add
        </button>
        <button type="button" onClick={() => navigate("/")} style={secondaryBtn}>
          Cancel
        </button>
      </div>
    </form>
  );
}

const label = { display: "block", fontSize: 12, color: "var(--text-muted)", marginBottom: 4, marginTop: 12 };
const input = {
  width: "100%",
  background: "var(--surface)",
  border: "1px solid var(--border)",
  color: "var(--text)",
  padding: "8px 12px",
  borderRadius: "var(--radius-card)",
  fontFamily: "inherit",
  fontSize: 14,
};
const primaryBtn = {
  background: "var(--accent)",
  color: "white",
  border: "none",
  padding: "8px 16px",
  borderRadius: "var(--radius-card)",
  cursor: "pointer",
};
const secondaryBtn = {
  background: "transparent",
  border: "1px solid var(--border)",
  color: "var(--text)",
  padding: "8px 16px",
  borderRadius: "var(--radius-card)",
  cursor: "pointer",
};