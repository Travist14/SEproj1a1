import { useEffect, useRef } from 'react';

export default function ChatWindow({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.map((message) => (
        <article
          key={message.id}
          className={`message message-${message.role}${message.pending ? ' message-pending' : ''}`}
        >
          <header className="message-meta">
            <span className="message-role">{labelForRole(message.role)}</span>
          </header>
          <p className="message-content">{message.content}</p>
          {message.error ? <p className="message-error">{message.error}</p> : null}
        </article>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}

function labelForRole(role) {
  switch (role) {
    case 'user':
      return 'You';
    case 'assistant':
      return 'Assistant';
    case 'system':
      return 'System';
    default:
      return role;
  }
}
