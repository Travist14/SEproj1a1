import { useCallback, useRef, useState } from 'react';
import ChatWindow from './components/ChatWindow.jsx';
import MessageInput from './components/MessageInput.jsx';
import Login from './components/Login.jsx';
import RequirementsPanel from './components/RequirementsPanel.jsx';
import { useChat } from './hooks/useChat.js';
import { useOrchestratorPlan } from './hooks/useOrchestratorPlan.js';
import { PERSONAS, getPersonaConfig } from './config/personas.js';

export default function App() {
  const [personaKey, setPersonaKey] = useState(null);
  const [splitRatio, setSplitRatio] = useState(65);
  const [isResizing, setIsResizing] = useState(false);
  const layoutRef = useRef(null);
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

  const adjustSplit = useCallback((deltaPercent) => {
    setSplitRatio((current) => {
      const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
      return clamp(current + deltaPercent, 50, 85);
    });
  }, []);

  const handleDividerPointerDown = useCallback((event) => {
    event.preventDefault();
    const container = layoutRef.current;
    if (!container) {
      return;
    }

    setIsResizing(true);
    const { width, left } = container.getBoundingClientRect();

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    const handlePointerMove = (moveEvent) => {
      const clientX = moveEvent.clientX;
      const relativeX = clientX - left;
      const percent = (relativeX / width) * 100;
      setSplitRatio(clamp(percent, 50, 85));
    };

    const stopResizing = () => {
      setIsResizing(false);
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerup', stopResizing);
      window.removeEventListener('pointercancel', stopResizing);
    };

    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerup', stopResizing, { once: true });
    window.addEventListener('pointercancel', stopResizing, { once: true });
  }, []);

  const handleDividerKeyDown = useCallback(
    (event) => {
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        adjustSplit(-3);
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        adjustSplit(3);
      }
    },
    [adjustSplit]
  );

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
      <main
        className="app-main"
        ref={layoutRef}
        data-resizing={isResizing ? 'true' : 'false'}
        style={{
          gridTemplateColumns: `${splitRatio}% 10px minmax(280px, 1fr)`
        }}
      >
        <section className="chat-section">
          <ChatWindow messages={messages} />
        </section>
        <div
          className="layout-divider"
          role="separator"
          aria-orientation="vertical"
          aria-label="Resize chat and plan panes"
          tabIndex={0}
          onPointerDown={handleDividerPointerDown}
          onKeyDown={handleDividerKeyDown}
        />
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
