# Frontend Architecture

Deep dive into the React frontend architecture, component structure, and state management.

## Technology Stack

- **React 18.3+**: UI library with hooks
- **Vite 5.1+**: Fast build tool and dev server
- **JavaScript (ES6+)**: Modern JavaScript features
- **CSS**: Custom styling with CSS variables

## Project Structure

```
src/frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ChatWindow.jsx   # Message display
│   │   ├── Login.jsx        # Persona selection
│   │   └── MessageInput.jsx # User input
│   ├── hooks/               # Custom React hooks
│   │   └── useChat.js       # Chat state management
│   ├── api/                 # API client
│   │   └── client.js        # HTTP/streaming client
│   ├── config/              # Configuration
│   │   └── personas.js      # Persona definitions
│   ├── App.jsx              # Root component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
└── index.html               # HTML template
```

## Core Components

### App Component

**File**: `src/frontend/src/App.jsx`

**Responsibilities**:
- Top-level routing (login vs main app)
- Persona state management
- Chat lifecycle coordination

**State**:
```javascript
const [personaKey, setPersonaKey] = useState(null);
const { messages, sendMessage, cancel, reset, status } = useChat(activePersona.key);
```

**Key Features**:
- Conditional rendering based on persona selection
- Integration with useChat hook
- Action buttons (Reset, Switch Role)

### ChatWindow Component

**File**: `src/frontend/src/components/ChatWindow.jsx`

**Purpose**: Display chat message history with role-based styling

**Props**:
```javascript
{
  messages: Array<{
    role: 'user' | 'assistant',
    content: string
  }>
}
```

**Features**:
- Auto-scroll to latest message
- Markdown rendering support
- Role-based message styling
- Empty state handling

### MessageInput Component

**File**: `src/frontend/src/components/MessageInput.jsx`

**Purpose**: User input with send/cancel controls

**Props**:
```javascript
{
  onSend: (message: string) => void,
  onCancel: () => void,
  disabled: boolean,
  status: 'idle' | 'pending' | 'error'
}
```

**Features**:
- Enter key to send
- Disabled state during generation
- Cancel button for streaming
- Auto-focus and auto-resize

### Login Component

**File**: `src/frontend/src/components/Login.jsx`

**Purpose**: Persona selection screen

**Props**:
```javascript
{
  personas: Object<string, PersonaConfig>,
  onSelect: (personaKey: string) => void
}
```

**Features**:
- Grid layout of persona cards
- Color-coded personas
- Hover effects
- Responsive design

## Custom Hooks

### useChat Hook

**File**: `src/frontend/src/hooks/useChat.js`

**Purpose**: Centralized chat state and API interaction

**Interface**:
```javascript
const {
  messages,      // Array of chat messages
  sendMessage,   // (content: string) => Promise<void>
  cancel,        // () => void
  reset,         // () => void
  status         // 'idle' | 'pending' | 'error'
} = useChat(personaKey);
```

**State Management**:
```javascript
const [messages, setMessages] = useState([]);
const [status, setStatus] = useState('idle');
const abortControllerRef = useRef(null);
```

**Key Features**:
- Async message sending with streaming
- Abort controller for cancellation
- Error handling and recovery
- Message history management

**Send Message Flow**:
1. Add user message to history
2. Set status to 'pending'
3. Create abort controller
4. Call streaming API
5. Accumulate tokens in assistant message
6. Update UI in real-time
7. Set status to 'idle' on completion

## API Client

### streamGenerate Function

**File**: `src/frontend/src/api/client.js`

**Purpose**: Handle streaming NDJSON responses from backend

**Signature**:
```javascript
async function streamGenerate(payload, onChunk, signal)
```

**Parameters**:
- `payload`: GenerateRequest object
- `onChunk`: Callback for each token chunk
- `signal`: AbortSignal for cancellation

**Implementation**:
```javascript
const response = await fetch(`${API_BASE_URL}/api/generate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload),
  signal
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split('\n').filter(Boolean);

  for (const line of lines) {
    const data = JSON.parse(line);
    if (data.type === 'token') {
      onChunk(data.delta);
    }
  }
}
```

## Configuration

### Personas Configuration

**File**: `src/frontend/src/config/personas.js`

**Structure**:
```javascript
export const PERSONAS = {
  developer: {
    key: 'developer',
    label: 'Developer',
    description: 'Technical feasibility and implementation concerns',
    systemPrompt: 'You are a software developer...',
    color: '#2563eb'
  },
  // ... other personas
};

export function getPersonaConfig(key) {
  return PERSONAS[key] || PERSONAS.developer;
}
```

**Persona Properties**:
- `key`: Unique identifier
- `label`: Display name
- `description`: Short description
- `systemPrompt`: LLM system message
- `color`: Theme color (hex)

### API Configuration

**File**: `src/frontend/src/api/client.js`

```javascript
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
export const DEFAULT_MAX_TOKENS = 512;
export const DEFAULT_TEMPERATURE = 0.7;
```

## State Management

### Local State Pattern

MARC uses React's built-in state management (useState, useReducer) rather than external libraries like Redux or Zustand.

**Rationale**:
- Simple application state
- No complex global state needs
- Better performance for small apps
- Easier to understand and maintain

**State Locations**:
- **App.jsx**: Persona selection
- **useChat**: Message history, status
- **Components**: Local UI state (input value, etc.)

## Styling

### CSS Variables

Global theme colors defined in `index.css`:

```css
:root {
  --color-developer: #2563eb;
  --color-pm: #059669;
  --color-customer: #dc2626;
  --color-sales: #7c3aed;
  --color-shareholder: #ea580c;
}
```

### Component Styling

- **Scoped classes**: Each component uses unique class names
- **BEM-like naming**: `.component__element--modifier`
- **Responsive**: Mobile-first approach with media queries

## Performance Optimizations

### Current Optimizations

1. **React.memo**: Prevent unnecessary re-renders (if needed)
2. **useCallback**: Memoize callbacks in useChat
3. **Streaming**: Real-time token display without waiting
4. **Debouncing**: Input debouncing for better UX

### Future Optimizations

1. **Code Splitting**: Lazy load components
```javascript
const ChatWindow = lazy(() => import('./components/ChatWindow'));
```

2. **Virtual Scrolling**: For long chat histories
3. **Service Worker**: Offline support and caching
4. **Bundle Size**: Analyze and reduce bundle size

## Error Handling

### Error Boundaries

Add error boundaries to catch component errors:

```javascript
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Component error:', error, errorInfo);
  }

  render() {
    return this.props.children;
  }
}
```

### API Error Handling

In useChat hook:

```javascript
try {
  await streamGenerate(payload, onChunk, signal);
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request cancelled');
  } else {
    setStatus('error');
    console.error('Generation failed:', error);
  }
}
```

## Testing Strategy

### Component Testing

Use React Testing Library:

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import MessageInput from './MessageInput';

test('sends message on enter key', () => {
  const onSend = jest.fn();
  render(<MessageInput onSend={onSend} />);

  const input = screen.getByRole('textbox');
  fireEvent.change(input, { target: { value: 'Test' } });
  fireEvent.keyPress(input, { key: 'Enter', code: 13 });

  expect(onSend).toHaveBeenCalledWith('Test');
});
```

### Hook Testing

Use React Hooks Testing Library:

```javascript
import { renderHook, act } from '@testing-library/react-hooks';
import { useChat } from './useChat';

test('sends message and updates history', async () => {
  const { result } = renderHook(() => useChat('developer'));

  await act(async () => {
    await result.current.sendMessage('Hello');
  });

  expect(result.current.messages).toHaveLength(2); // user + assistant
});
```

## Build & Deployment

### Development

```bash
npm run dev
```

Features:
- Hot Module Replacement (HMR)
- Fast refresh
- Source maps

### Production Build

```bash
npm run build
```

Output:
- Minified JavaScript
- Optimized CSS
- Asset fingerprinting
- Tree-shaken bundles

### Preview Production Build

```bash
npm run preview
```

## Next Steps

- [Backend Architecture](backend.md) - Backend design patterns
- [Multi-Agent System](multi-agent.md) - Planned features
- [API Reference](../api/frontend.md) - Component API docs
