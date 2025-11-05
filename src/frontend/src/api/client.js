const API_BASE_URL = import.meta.env.VITE_BACKEND_API_BASE?.replace(/\/+$/, '') ?? '/api';
const GENERATE_ROUTE = `${API_BASE_URL}/generate`;
const HEALTH_ROUTE = `${API_BASE_URL}/health`;

/**
 * Basic client helper for talking to the FastAPI backend.
 * - Sends the full message list to the backend.
 * - Always requests a non-streaming response.
 */
export async function generateCompletion(messages, { signal, persona } = {}) {
  const response = await fetch(GENERATE_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages,
      stream: false,
      persona: persona || undefined
    }),
    signal
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const payload = await response.json().catch(() => ({}));
  const output = typeof payload.output === 'string' ? payload.output : '';
  return output;
}

export async function pingBackend() {
  const response = await fetch(HEALTH_ROUTE);
  return response.ok;
}
