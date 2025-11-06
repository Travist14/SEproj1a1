import { useCallback, useEffect, useRef, useState } from 'react';
import { fetchOrchestratorState } from '../api/client';

const DEFAULT_REFRESH_INTERVAL = 15000;

export function useOrchestratorPlan(chatStatus) {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const statusRef = useRef(chatStatus);
  const refreshRef = useRef(null);

  const refresh = useCallback(async () => {
    try {
      const state = await fetchOrchestratorState();
      setPlan(state);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const timer = setInterval(() => {
      refreshRef.current?.();
    }, DEFAULT_REFRESH_INTERVAL);
    refreshRef.current = refresh;
    return () => {
      refreshRef.current = null;
      clearInterval(timer);
    };
  }, [refresh]);

  useEffect(() => {
    const previous = statusRef.current;
    statusRef.current = chatStatus;
    if (previous === 'pending' && chatStatus === 'idle') {
      refresh();
    }
  }, [chatStatus, refresh]);

  return { plan, loading, error, refresh };
}
