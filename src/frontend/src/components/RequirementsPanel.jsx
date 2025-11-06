export default function RequirementsPanel({
  plan,
  loading,
  error,
  onRefresh,
  onGenerate,
  generating
}) {
  const hasSummaries = Boolean(plan?.summaries && Object.keys(plan.summaries).length > 0);
  const hasDocument = Boolean(plan?.requirementsDocument);

  const handleDownload = () => {
    if (!hasDocument) {
      return;
    }
    const timestamp = plan?.updatedAt ? new Date(plan.updatedAt).toISOString().replace(/[:.]/g, '-') : 'latest';
    const filename = `requirements-plan-${timestamp}.txt`;
    const blob = new Blob([plan.requirementsDocument], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.rel = 'noopener noreferrer';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

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

      {loading && !hasSummaries ? <p className="requirements-status">Loading orchestration summaries…</p> : null}
      {error ? (
        <p className="requirements-status requirements-error">Failed to load plan: {error.message}</p>
      ) : null}

      {hasSummaries ? (
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
            {hasDocument ? (
              <>
                <div className="requirements-actions">
                  <button
                    type="button"
                    className="secondary"
                    onClick={onGenerate}
                    disabled={generating}
                  >
                    {generating ? 'Generating…' : 'Regenerate Document'}
                  </button>
                  <button type="button" onClick={handleDownload}>
                    Download
                  </button>
                </div>
                <pre className="requirements-document">{plan.requirementsDocument}</pre>
              </>
            ) : (
              <div className="requirements-empty">
                <p>
                  The requirements document has not been generated yet. Click the button below to compile it from the
                  latest stakeholder summaries.
                </p>
                <button type="button" onClick={onGenerate} disabled={generating || loading}>
                  {generating ? 'Generating…' : 'Generate Requirements Document'}
                </button>
              </div>
            )}
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
