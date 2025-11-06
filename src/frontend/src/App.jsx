import { useState } from 'react';
import ChatWindow from './components/ChatWindow.jsx';
import MessageInput from './components/MessageInput.jsx';
import Login from './components/Login.jsx';
import RequirementsPanel from './components/RequirementsPanel.jsx';
import { useChat } from './hooks/useChat.js';
import { useOrchestratorPlan } from './hooks/useOrchestratorPlan.js';
import { PERSONAS, getPersonaConfig } from './config/personas.js';

export default function App() {
  const [personaKey, setPersonaKey] = useState(null);
  const activePersona = getPersonaConfig(personaKey ?? 'developer');
  const { messages, sendMessage, cancel, reset, status } = useChat(activePersona.key);
  const {
    plan: orchestratorPlan,
    loading: planLoading,
    error: planError,
    refresh: refreshPlan,
    generateRequirements,
    generating: generatingRequirements
  } = useOrchestratorPlan(status);

  if (!personaKey) {
    return (
      <div className="login-screen">
        <Login personas={PERSONAS} onSelect={setPersonaKey} />
      </div>
    );
  }

  const handleSwitchPersona = () => {
    setPersonaKey(null);
  };

  const handleReset = () => {
    reset();
  };

  return (
    <div className={`app-shell app-shell-${activePersona.key}`}>
      <header className="app-header">
        <h1>MARC</h1>
        <div className="header-actions">
          <div className={`persona-badge persona-${activePersona.key}`}>{activePersona.label}</div>
          <button type="button" onClick={handleReset} className="secondary">
            Reset Chat
          </button>
          <button type="button" onClick={handleSwitchPersona} className="secondary">
            Switch Role
          </button>
        </div>
      </header>
      <main className="app-main">
        <section className="chat-section">
          <ChatWindow messages={messages} />
        </section>
        <aside className="plan-section">
          <RequirementsPanel
            plan={orchestratorPlan}
            loading={planLoading}
            error={planError}
            onRefresh={refreshPlan}
            onGenerate={generateRequirements}
            generating={generatingRequirements}
          />
        </aside>
      </main>
      <footer className="app-footer">
        <MessageInput
          onSend={sendMessage}
          onCancel={cancel}
          disabled={status === 'pending'}
          status={status}
        />
        {status === 'pending' ? <span className="status">Generating response...</span> : null}
        {status === 'error' ? <span className="status status-error">Last request failed.</span> : null}
      </footer>
    </div>
  );
}
