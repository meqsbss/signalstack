export default function SkeletonRows({ rows = 5 }: { rows?: number }) {
  return (
    <div>
      {Array.from({ length: rows }).map((_, i) => (
        <div
          key={i}
          style={{
            height: 40,
            marginBottom: 4,
            borderRadius: "var(--radius-card)",
            background: "var(--surface-raised)",
            opacity: 0.5,
            animation: "pulse 1.4s ease-in-out infinite",
          }}
        />
      ))}
      <style>{`@keyframes pulse { 0%,100% { opacity: 0.3 } 50% { opacity: 0.6 } }`}</style>
    </div>
  );
}