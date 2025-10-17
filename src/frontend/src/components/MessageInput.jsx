import { useState } from 'react';

export default function MessageInput({ onSend, onCancel, disabled, status }) {
  const [value, setValue] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!value.trim()) {
      return;
    }
    onSend(value);
    setValue('');
  };

  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <textarea
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Ask the assistant something..."
        rows={3}
        disabled={disabled}
      />
      <div className="message-input-actions">
        <button type="submit" disabled={disabled}>
          Send
        </button>
        {status === 'pending' ? (
          <button type="button" onClick={onCancel} className="secondary">
            Stop
          </button>
        ) : null}
      </div>
    </form>
  );
}
