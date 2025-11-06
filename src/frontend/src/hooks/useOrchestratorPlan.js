import { useCallback, useEffect, useRef, useState } from 'react';
import { fetchOrchestratorState, runOrchestrator } from '../api/client';

const DEFAULT_REFRESH_INTERVAL = 15000;

export function useOrchestratorPlan(chatStatus) {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [generating, setGenerating] = useState(false);
  const statusRef = useRef(chatStatus);
  const refreshRef = useRef(null);

  const refresh = useCallback(async () => {
    try {
      const state = await fetchOrchestratorState();
      setPlan(state);
      setError(null);
      return state;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh().catch(() => {
      /* handled via error state */
    });
    const timer = setInterval(() => {
      const fn = refreshRef.current;
      if (fn) {
        fn().catch(() => {
          /* handled via error state */
        });
      }
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
      refresh().catch(() => {
        /* handled via error state */
      });
    }
  }, [chatStatus, refresh]);

  const generateRequirements = useCallback(async () => {
    if (generating) {
      return;
    }
    setGenerating(true);
    try {
      setError(null);
      const result = await runOrchestrator({ include_requirements: true });
      setPlan((prev) => ({
        updatedAt: new Date().toISOString(),
        summaries: result.summaries ?? prev?.summaries ?? {},
        requirementsDocument: result.requirementsDocument ?? '',
      }));
      await refresh();
    } catch (err) {
      setError(err);
    } finally {
      setGenerating(false);
    }
  }, [generating, refresh]);

  return { plan, loading, error, refresh, generateRequirements, generating };
}
