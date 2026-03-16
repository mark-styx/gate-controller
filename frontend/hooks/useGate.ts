import { useState, useEffect, useCallback, useRef } from 'react';
import { gateApi, GateStatus, HealthStatus } from '@/lib/api';

export function useGateStatus(refreshInterval: number = 2000) {
  const [status, setStatus] = useState<GateStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      const data = await gateApi.getStatus();
      setStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch status');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();

    if (refreshInterval > 0) {
      intervalRef.current = setInterval(fetchStatus, refreshInterval);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [fetchStatus, refreshInterval]);

  return { status, loading, error, refetch: fetchStatus };
}

export function useHealth() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = useCallback(async () => {
    try {
      const data = await gateApi.getHealth();
      setHealth(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Health check failed');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  return { health, loading, error, refetch: checkHealth };
}

export function useGateControl() {
  const [activating, setActivating] = useState(false);
  const [togglingEbrake, setTogglingEbrake] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const activate = useCallback(async () => {
    setActivating(true);
    setError(null);
    try {
      const result = await gateApi.activate();
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Activation failed';
      setError(message);
      throw err;
    } finally {
      setActivating(false);
    }
  }, []);

  const toggleEbrake = useCallback(async () => {
    setTogglingEbrake(true);
    setError(null);
    try {
      const result = await gateApi.toggleEbrake();
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Toggle ebrake failed';
      setError(message);
      throw err;
    } finally {
      setTogglingEbrake(false);
    }
  }, []);

  return {
    activate,
    toggleEbrake,
    activating,
    togglingEbrake,
    error,
    clearError: () => setError(null),
  };
}
