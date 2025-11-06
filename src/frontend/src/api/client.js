const API_BASE_URL = import.meta.env.VITE_BACKEND_API_BASE?.replace(/\/+$/, '') ?? '/api';
const GENERATE_ROUTE = `${API_BASE_URL}/generate`;
const HEALTH_ROUTE = `${API_BASE_URL}/health`;
const ORCHESTRATE_ROUTE = `${API_BASE_URL}/orchestrate`;
const ORCHESTRATOR_STATE_ROUTE = `${API_BASE_URL}/orchestrator/state`;

function parseEventLine(line) {
  if (!line) {
    return null;
  }

  let payload;
  try {
    payload = JSON.parse(line);
  } catch (error) {
    console.warn('[api] Failed to parse stream chunk:', line, error);
    return null;
  }

  const type = payload.type ?? 'token';
  const requestId = payload.request_id;

  switch (type) {
    case 'token':
      return {
        type: 'token',
        delta: typeof payload.delta === 'string' ? payload.delta : '',
        content: typeof payload.content === 'string' ? payload.content : null,
        requestId
      };
    case 'done':
      return {
        type: 'done',
        content: typeof payload.content === 'string' ? payload.content : '',
        finishReason: payload.finish_reason ?? null,
        requestId
      };
    case 'error': {
      const message = typeof payload.message === 'string' ? payload.message : 'Generation failed.';
      const error = new Error(message);
      error.name = 'RemoteError';
      error.requestId = requestId;
      throw error;
    }
    default:
      console.debug('[api] Received unhandled stream event:', payload);
      return null;
  }
}

function processBuffer(buffer, { final = false } = {}) {
  const events = [];
  let working = buffer;

  while (true) {
    const index = working.indexOf('\n');
    if (index === -1) {
      break;
    }

    const line = working.slice(0, index).trim();
    working = working.slice(index + 1);
    const event = parseEventLine(line);
    if (event) {
      events.push(event);
    }
  }

  if (final) {
    const remaining = working.trim();
    if (remaining) {
      const event = parseEventLine(remaining);
      if (event) {
        events.push(event);
      }
      working = '';
    }
  }

  return { events, remainder: working };
}

export async function* streamCompletion(messages, { signal, persona } = {}) {
  const response = await fetch(GENERATE_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages,
      stream: true,
      persona: persona || undefined
    }),
    signal
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  if (!response.body) {
    throw new Error('Streaming is not supported in this environment.');
  }

  const reader = response.body.getReader();
  let buffer = '';
  const decoder = new TextDecoder();

  const cancelOnAbort = signal
    ? () =>
        reader
          .cancel()
          .catch(() => {
            /* no-op */
          })
    : null;

  if (signal?.aborted) {
    cancelOnAbort?.();
    throw new DOMException('Aborted', 'AbortError');
  }

  if (signal && cancelOnAbort) {
    signal.addEventListener('abort', cancelOnAbort, { once: true });
  }

  try {
    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        buffer += decoder.decode();
        const { events } = processBuffer(buffer, { final: true });
        for (const event of events) {
          yield event;
          if (event.type === 'done') {
            return;
          }
        }
        return;
      }

      buffer += decoder.decode(value, { stream: true });
      const { events, remainder } = processBuffer(buffer);
      buffer = remainder;

      for (const event of events) {
        yield event;
        if (event.type === 'done') {
          return;
        }
      }
    }
  } finally {
    if (signal && cancelOnAbort) {
      signal.removeEventListener('abort', cancelOnAbort);
    }
    reader.releaseLock();
  }
}

/**
 * Helper for callers that want the full response rather than a stream.
 * When stream=true it will internally consume the stream and return the accumulated text.
 */
export async function generateCompletion(messages, { signal, persona, stream = false } = {}) {
  if (stream) {
    let accumulated = '';
    for await (const event of streamCompletion(messages, { signal, persona })) {
      if (event.type === 'token') {
        accumulated += event.delta;
      } else if (event.type === 'done' && !accumulated) {
        accumulated = event.content ?? '';
      }
    }
    return accumulated;
  }

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

export async function fetchOrchestratorState() {
  const response = await fetch(ORCHESTRATOR_STATE_ROUTE);

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Failed to load orchestrator state (status ${response.status})`);
  }

  const payload = await response.json();
  return {
    updatedAt: payload.updated_at ?? null,
    summaries: payload.summaries ?? {},
    requirementsDocument: payload.requirements_document ?? ''
  };
}

export async function runOrchestrator(request = {}) {
  const response = await fetch(ORCHESTRATE_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    throw new Error(`Failed to run orchestrator (status ${response.status})`);
  }

  const payload = await response.json();
  return {
    summaries: payload.summaries ?? {},
    requirementsDocument: payload.requirements_document ?? ''
  };
}
