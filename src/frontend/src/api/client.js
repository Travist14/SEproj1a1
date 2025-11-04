const API_BASE_URL = import.meta.env.VITE_VLLM_API_BASE?.replace(/\/+$/, '') ?? 'http://localhost:8001';
const CHAT_COMPLETIONS_ROUTE = `${API_BASE_URL}/v1/chat/completions`;
const MODELS_ROUTE = `${API_BASE_URL}/v1/models`;
const DEFAULT_MODEL = import.meta.env.VITE_VLLM_MODEL ?? 'meta-llama/Llama-3.1-8B-Instruct';

/**
 * Basic client helper for talking to the vLLM-backed API.
 * - Sends the full message list to the backend.
 * - Supports optional streaming callbacks compatible with SSE-style outputs.
 */
export async function generateCompletion(messages, { onToken, signal, persona } = {}) {
  const response = await fetch(CHAT_COMPLETIONS_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages,
      stream: Boolean(onToken),
      model: DEFAULT_MODEL,
      metadata: persona ? { persona } : undefined
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
  const output =
    payload.choices?.[0]?.message?.content ??
    payload.output ??
    payload.text ??
    '';
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
      try {
        const data = JSON.parse(payload);
        const delta = data.choices?.[0]?.delta?.content;
        if (delta) {
          onToken(delta);
          aggregate += delta;
        }
      } catch {
        // Ignore malformed payloads but continue streaming
        continue;
      }
    }
  }
  return aggregate;
}

export async function pingBackend() {
  const response = await fetch(MODELS_ROUTE);
  return response.ok;
}
