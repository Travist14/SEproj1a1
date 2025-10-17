export default function Login({ personas, onSelect }) {
  return (
    <div className="login-card">
      <h1>Welcome to the vLLM Chat Playground</h1>
      <p className="login-subtitle">Choose a workspace to tailor the assistant to your needs.</p>
      <div className="login-options">
        {Object.values(personas).map((persona) => (
          <button
            key={persona.key}
            type="button"
            className={`login-option persona-${persona.key}`}
            onClick={() => onSelect(persona.key)}
          >
            <span className="login-option-label">{persona.label}</span>
            <span className="login-option-description">{persona.description}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
