# Frontend Component API

Documentation for React components and hooks.

## Components

### App

**File**: `src/frontend/src/App.jsx`

**Purpose**: Root application component

**State**:
- `personaKey`: Currently selected persona (null = login screen)

**Props**: None

**Example**:
```jsx
import App from './App';

<App />
```

---

### ChatWindow

**File**: `src/frontend/src/components/ChatWindow.jsx`

**Purpose**: Display chat message history

**Props**:
```typescript
{
  messages: Array<{
    role: 'user' | 'assistant',
    content: string
  }>
}
```

**Features**:
- Auto-scrolls to latest message
- Role-based styling
- Empty state message

**Example**:
```jsx
<ChatWindow messages={[
  { role: 'user', content: 'Hello' },
  { role: 'assistant', content: 'Hi there!' }
]} />
```

---

### MessageInput

**File**: `src/frontend/src/components/MessageInput.jsx`

**Purpose**: Text input for user messages

**Props**:
```typescript
{
  onSend: (message: string) => void,
  onCancel: () => void,
  disabled: boolean,
  status: 'idle' | 'pending' | 'error'
}
```

**Features**:
- Enter key to send
- Disabled during generation
- Cancel button when pending
- Auto-resize textarea

**Example**:
```jsx
<MessageInput
  onSend={(msg) => console.log(msg)}
  onCancel={() => console.log('Cancelled')}
  disabled={false}
  status="idle"
/>
```

---

### Login

**File**: `src/frontend/src/components/Login.jsx`

**Purpose**: Persona selection screen

**Props**:
```typescript
{
  personas: Record<string, PersonaConfig>,
  onSelect: (personaKey: string) => void
}
```

**PersonaConfig**:
```typescript
{
  key: string,
  label: string,
  description: string,
  color: string
}
```

**Example**:
```jsx
<Login
  personas={PERSONAS}
  onSelect={(key) => setPersona(key)}
/>
```

---

## Hooks

### useChat

**File**: `src/frontend/src/hooks/useChat.js`

**Purpose**: Manage chat state and API interactions

**Signature**:
```typescript
function useChat(personaKey: string): {
  messages: Array<Message>,
  sendMessage: (content: string) => Promise<void>,
  cancel: () => void,
  reset: () => void,
  status: 'idle' | 'pending' | 'error'
}
```

**Parameters**:
- `personaKey`: Selected persona identifier

**Returns**:
- `messages`: Array of chat messages
- `sendMessage`: Send user message and get response
- `cancel`: Cancel ongoing generation
- `reset`: Clear chat history
- `status`: Current generation status

**Example**:
```javascript
import { useChat } from './hooks/useChat';

function ChatApp() {
  const { messages, sendMessage, status } = useChat('developer');

  const handleSend = async (text) => {
    await sendMessage(text);
  };

  return (
    <>
      <ChatWindow messages={messages} />
      <MessageInput
        onSend={handleSend}
        disabled={status === 'pending'}
      />
    </>
  );
}
```

**State Management**:
- Maintains message history
- Tracks generation status
- Manages abort controller for cancellation

**Error Handling**:
- Sets status to 'error' on failure
- Logs errors to console
- Handles abort gracefully

---

## API Client

### streamGenerate

**File**: `src/frontend/src/api/client.js`

**Purpose**: Stream generation from backend API

**Signature**:
```typescript
async function streamGenerate(
  payload: GenerateRequest,
  onChunk: (delta: string) => void,
  signal?: AbortSignal
): Promise<void>
```

**Parameters**:
- `payload`: Request object matching GenerateRequest
- `onChunk`: Callback for each token chunk
- `signal`: Optional AbortSignal for cancellation

**Throws**:
- `Error`: If response is not OK
- `AbortError`: If request is cancelled

**Example**:
```javascript
import { streamGenerate } from './api/client';

const controller = new AbortController();

await streamGenerate(
  {
    messages: [
      { role: 'user', content: 'Hello' }
    ],
    stream: true
  },
  (delta) => {
    console.log('Token:', delta);
  },
  controller.signal
);

// To cancel:
controller.abort();
```

**Protocol**:
- Sends POST to /api/generate
- Reads NDJSON stream
- Parses each line as JSON
- Calls onChunk for token events
- Throws on error events

---

## Configuration

### PERSONAS

**File**: `src/frontend/src/config/personas.js`

**Purpose**: Persona definitions

**Type**:
```typescript
Record<string, {
  key: string,
  label: string,
  description: string,
  systemPrompt: string,
  color: string
}>
```

**Available Personas**:
- `developer`
- `product_manager`
- `customer`
- `sales`
- `shareholder`

**Example**:
```javascript
import { PERSONAS, getPersonaConfig } from './config/personas';

const dev = getPersonaConfig('developer');
console.log(dev.label); // "Developer"
console.log(dev.systemPrompt); // "You are a software developer..."
```

---

### getPersonaConfig

**File**: `src/frontend/src/config/personas.js`

**Purpose**: Get persona configuration by key

**Signature**:
```typescript
function getPersonaConfig(key: string): PersonaConfig
```

**Parameters**:
- `key`: Persona identifier

**Returns**: PersonaConfig object (defaults to 'developer' if not found)

**Example**:
```javascript
const persona = getPersonaConfig('product_manager');
```

---

## Styling

### CSS Classes

**Chat Window**:
- `.chat-window` - Container
- `.message` - Individual message
- `.message.user` - User message
- `.message.assistant` - Assistant message

**Message Input**:
- `.message-input` - Container
- `.message-input textarea` - Text input
- `.message-input button` - Send/cancel buttons

**Login**:
- `.login-screen` - Container
- `.persona-card` - Persona selection card
- `.persona-card-{key}` - Persona-specific styling

**App Shell**:
- `.app-shell` - Main container
- `.app-shell-{persona}` - Persona-themed app
- `.app-header` - Header
- `.app-main` - Main content
- `.app-footer` - Footer with input

---

## Next Steps

- [REST API](rest-api.md) - Backend API reference
- [Backend Modules](backend.md) - Python documentation
- [Frontend Architecture](../architecture/frontend.md) - Design patterns
