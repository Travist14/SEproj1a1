export default function RequirementsPanel({ plan, loading, error, onRefresh }) {
  const hasPlan = Boolean(plan?.requirementsDocument);

  return (
    <div className="requirements-panel">
      <header className="requirements-header">
        <div>
          <h2>Requirements Plan</h2>
          {plan?.updatedAt ? (
            <span className="requirements-updated">
              Updated {new Date(plan.updatedAt).toLocaleString()}
            </span>
          ) : null}
        </div>
        <button type="button" className="secondary" onClick={onRefresh} disabled={loading}>
          Refresh
        </button>
      </header>

      {loading && !hasPlan ? <p className="requirements-status">Loading orchestrator plan…</p> : null}
      {error ? (
        <p className="requirements-status requirements-error">Failed to load plan: {error.message}</p>
      ) : null}

      {hasPlan ? (
        <>
          <section className="requirements-section">
            <h3>Stakeholder Summaries</h3>
            <ul className="requirements-summaries">
              {Object.entries(plan.summaries ?? {}).map(([persona, summary]) => (
                <li key={persona}>
                  <h4>{formatPersonaLabel(persona)}</h4>
                  <p>{summary}</p>
                </li>
              ))}
            </ul>
          </section>
          <section className="requirements-section">
            <h3>Requirements Engineering Document</h3>
            <pre className="requirements-document">{plan.requirementsDocument}</pre>
          </section>
        </>
      ) : !loading && !error ? (
        <p className="requirements-status">No orchestrator plan available yet.</p>
      ) : null}
    </div>
  );
}

function formatPersonaLabel(persona) {
  if (!persona) {
    return 'General';
  }
  return persona
    .split(/[\s_-]+/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}
