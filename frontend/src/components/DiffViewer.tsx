export default function DiffViewer({ diff }: { diff: string }) {
  const lines = diff.split("\n");
  return (
    <pre
      style={{
        background: "var(--surface)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-card)",
        padding: 12,
        fontFamily: "var(--font-mono)",
        fontSize: 13,
        overflowX: "auto",
        margin: "8px 0 0",
      }}
    >
      {lines.map((line, i) => {
        const color = line.startsWith("+")
          ? "var(--success)"
          : line.startsWith("-")
          ? "var(--danger)"
          : "var(--text-muted)";
        return (
          <div key={i} style={{ color }}>
            {line || " "}
          </div>
        );
      })}
    </pre>
  );
}