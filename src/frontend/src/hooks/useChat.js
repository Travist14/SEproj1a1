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
      const assistantMessage = createMessage('assistant', '', { pending: true });

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
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessage.id
                  ? {
                      ...msg,
                      content: accumulated,
                      pending: true
                    }
                  : msg
              )
            );
          } else if (event.type === 'done' && !receivedToken) {
            accumulated = event.content ?? '';
          }
        }

        const normalized = (accumulated ?? '').trim();

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessage.id
              ? {
                  ...msg,
                  content: normalized || 'I was unable to generate a response. Please try again.',
                  pending: false
                }
              : msg
          )
        );
        setStatus('idle');
      } catch (error) {
        if (error.name === 'AbortError') {
          const normalized = (accumulated ?? '').trim();
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessage.id
                ? {
                    ...msg,
                    content: normalized || 'Generation cancelled.',
                    pending: false,
                    cancelled: true
                  }
                : msg
            )
          );
          setStatus('idle');
        } else {
          setStatus('error');
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessage.id
                ? {
                    ...msg,
                    content:
                      (accumulated ?? '').trim() || msg.content || 'Something went wrong. Please try again.',
                    pending: false,
                    error: error.message
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
