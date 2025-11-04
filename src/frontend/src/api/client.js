const API_BASE_URL = import.meta.env.VITE_BACKEND_API_BASE?.replace(/\/+$/, '') ?? '/api';
const GENERATE_ROUTE = `${API_BASE_URL}/generate`;
const HEALTH_ROUTE = `${API_BASE_URL}/health`;

/**
 * Basic client helper for talking to the FastAPI backend.
 * - Sends the full message list to the backend.
 * - Supports optional streaming callbacks compatible with SSE-style outputs.
 */
export async function generateCompletion(messages, { onToken, signal, persona } = {}) {
  const response = await fetch(GENERATE_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages,
      stream: Boolean(onToken),
      persona: persona || undefined
    }),
    signal
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const contentType = response.headers.get('content-type') ?? '';

  if (onToken && contentType.includes('text/event-stream')) {
    return handleStream(response, onToken);
  }

  const payload = await response.json().catch(() => ({}));
  const output = typeof payload.output === 'string' ? payload.output : '';
  if (output && onToken) {
    onToken(output);
  }
  return output;
}

async function handleStream(response, onToken) {
  const reader = response.body?.getReader();
  if (!reader) {
    return '';
  }

  const decoder = new TextDecoder();
  let aggregate = '';
  let buffer = '';
  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith('data:')) {
        continue;
      }
      const payload = trimmed.slice(5).trim();
      if (!payload) {
        continue;
      }
      if (payload === '[DONE]') {
        return aggregate;
      }
      if (payload.startsWith('ERROR:')) {
        throw new Error(payload.slice(6).trim() || 'Stream error');
      }
      onToken(payload);
      aggregate += payload;
    }
  }
  return aggregate;
}

export async function pingBackend() {
  const response = await fetch(HEALTH_ROUTE);
  return response.ok;
}
