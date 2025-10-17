const API_ROUTE = '/api/generate';

/**
 * Basic client helper for talking to the vLLM-backed API.
 * - Sends the full message list to the backend.
 * - Supports optional streaming callbacks compatible with SSE-style outputs.
 */
export async function generateCompletion(messages, { onToken, signal, persona } = {}) {
  const response = await fetch(API_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages,
      stream: Boolean(onToken),
      persona
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
  const output = payload.output ?? payload.text ?? '';
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
  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    const chunk = decoder.decode(value, { stream: true });
    const lines = chunk.split('\n');
    for (const line of lines) {
      if (!line.startsWith('data: ')) {
        continue;
      }
      const payload = line.slice(6).trim();
      if (!payload || payload === '[DONE]') {
        continue;
      }
      onToken(payload);
      aggregate += payload;
    }
  }
  return aggregate;
}

export async function pingBackend() {
  const response = await fetch('/api/health');
  return response.ok;
}
