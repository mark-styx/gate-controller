'use client';

import { useHealth } from '@/hooks/useGate';
import { useEffect, useState } from 'react';

export default function HealthIndicator() {
  const { health, loading, error, refetch } = useHealth();
  const [lastCheck, setLastCheck] = useState<Date>(new Date());

  useEffect(() => {
    if (health) {
      setLastCheck(new Date());
    }
  }, [health]);

  const getStatusColor = () => {
    if (loading) return 'bg-yellow-500';
    if (error || health?.status !== 'healthy') return 'bg-red-500';
    return 'bg-green-500';
  };

  const getStatusText = () => {
    if (loading) return 'Checking...';
    if (error) return 'Connection Error';
    if (health?.status === 'healthy') return 'System Healthy';
    return 'System Issues';
  };

  return (
    <div 
      className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
      onClick={() => refetch()}
      title={`Last checked: ${lastCheck.toLocaleTimeString()}`}
    >
      <div className={`w-2 h-2 rounded-full ${getStatusColor()} ${!loading && 'animate-pulse'}`} />
      <span className="text-xs text-gray-400">{getStatusText()}</span>
    </div>
  );
}
