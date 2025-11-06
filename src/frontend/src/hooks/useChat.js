import { useState, useCallback, useRef, useEffect } from 'react';
import { streamCompletion } from '../api/client';
import { getPersonaConfig } from '../config/personas';

function systemMessageForPersona(personaKey) {
  const persona = getPersonaConfig(personaKey);
  return {
    id: `system-${persona.key}`,
    role: 'system',
    content: persona.systemPrompt
  };
}

function createMessage(role, content, extras = {}) {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
    role,
    content,
    ...extras
  };
}

function splitReasoningContent(text) {
  if (!text) {
    return { visible: '', reasoning: '' };
  }

  const patterns = [
    { open: '<think>', close: '</think>' },
    { open: '<thinking>', close: '</thinking>' },
    { open: '<THINK>', close: '</THINK>' }
  ];

  let reasoningSegments = [];
  let visibleSegments = [];
  let remainder = text;
  let sawReasoning = false;

  while (remainder.length > 0) {
    let earliestMatch = null;

    for (const pattern of patterns) {
      const index = remainder.indexOf(pattern.open);
      if (index !== -1 && (earliestMatch === null || index < earliestMatch.index)) {
        earliestMatch = { ...pattern, index };
      }
    }

    if (!earliestMatch) {
      visibleSegments.push(remainder);
      break;
    }

    if (earliestMatch.index > 0) {
      visibleSegments.push(remainder.slice(0, earliestMatch.index));
    }

    remainder = remainder.slice(earliestMatch.index + earliestMatch.open.length);
    const closeIndex = remainder.indexOf(earliestMatch.close);

    if (closeIndex === -1) {
      reasoningSegments.push(remainder);
      sawReasoning = true;
      remainder = '';
      break;
    }

    reasoningSegments.push(remainder.slice(0, closeIndex));
    sawReasoning = true;
    remainder = remainder.slice(closeIndex + earliestMatch.close.length);
  }

  const visible = visibleSegments.join('');
  const reasoning = reasoningSegments.join('').trim();

  return {
    visible: sawReasoning ? visible.replace(/^\s+/, '') : visible,
    reasoning
  };
}

export function useChat(personaKey = 'developer') {
  const [messages, setMessages] = useState(() => [systemMessageForPersona(personaKey)]);
  const [status, setStatus] = useState('idle');
  const abortRef = useRef(null);
  const personaRef = useRef(personaKey);

  useEffect(() => {
    if (personaRef.current !== personaKey) {
      personaRef.current = personaKey;
      setMessages([systemMessageForPersona(personaKey)]);
      setStatus('idle');
    }
  }, [personaKey]);

  const sendMessage = useCallback(
    async (input) => {
      const content = input.trim();
      if (!content) {
        return;
      }

      const userMessage = createMessage('user', content);
      const assistantMessage = createMessage('assistant', '', { pending: true, reasoning: '', raw: '' });

      setMessages((prev) => [...prev, userMessage, assistantMessage]);
      setStatus('pending');

      const controller = new AbortController();
      abortRef.current = controller;

      let accumulated = '';
      let receivedToken = false;

      try {
        const apiMessages = messages
          .filter((msg) => !msg.pending)
          .map((msg) => ({ role: msg.role, content: msg.content }))
          .concat({ role: 'user', content });

        for await (const event of streamCompletion(apiMessages, {
          signal: controller.signal,
          persona: personaRef.current
        })) {
          if (event.type === 'token') {
            receivedToken = true;
            accumulated += event.delta ?? '';
            console.debug('[chat] Token chunk:', event.delta ?? '');
            const { visible, reasoning } = splitReasoningContent(accumulated);
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessage.id
                  ? {
                      ...msg,
                      content: visible,
                      pending: true,
                      reasoning,
                      raw: accumulated
                    }
                  : msg
              )
            );
          } else if (event.type === 'done' && !receivedToken) {
            accumulated = event.content ?? '';
          }
        }

        const normalized = (accumulated ?? '').trim();
        const { visible, reasoning } = splitReasoningContent(normalized);

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessage.id
              ? {
                  ...msg,
                  content: visible || 'I was unable to generate a response. Please try again.',
                  pending: false,
                  reasoning,
                  raw: normalized
                }
              : msg
          )
        );
        setStatus('idle');
      } catch (error) {
        if (error.name === 'AbortError') {
          const normalized = (accumulated ?? '').trim();
          const { visible, reasoning } = splitReasoningContent(normalized);
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessage.id
                ? {
                    ...msg,
                    content: visible || 'Generation cancelled.',
                    pending: false,
                    cancelled: true,
                    reasoning,
                    raw: normalized
                  }
                : msg
            )
          );
          setStatus('idle');
        } else {
          setStatus('error');
          const trimmed = (accumulated ?? '').trim();
          const { visible, reasoning } = splitReasoningContent(trimmed);
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessage.id
                ? {
                    ...msg,
                    content: visible || msg.content || 'Something went wrong. Please try again.',
                    pending: false,
                    error: error.message,
                    reasoning,
                    raw: trimmed
                  }
                : msg
            )
          );
        }
      } finally {
        abortRef.current = null;
      }
    },
    [messages]
  );

  const cancel = useCallback(() => {
    if (abortRef.current) {
      abortRef.current.abort();
    }
  }, []);

  const reset = useCallback(() => {
    cancel();
    setMessages([systemMessageForPersona(personaRef.current)]);
    setStatus('idle');
  }, [cancel]);

  return { messages, sendMessage, cancel, reset, status };
}
