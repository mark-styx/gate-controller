'use client';

import { useGateStatus, useGateControl } from '@/hooks/useGate';
import { useState, useEffect } from 'react';

export default function Home() {
  const { status, loading, error, refetch } = useGateStatus(2000);
  const { activate, toggleEbrake, activating, togglingEbrake, error: controlError, clearError } = useGateControl();
  const [showSuccess, setShowSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (controlError) {
      const timer = setTimeout(clearError, 5000);
      return () => clearTimeout(timer);
    }
  }, [controlError, clearError]);

  useEffect(() => {
    if (showSuccess) {
      const timer = setTimeout(() => setShowSuccess(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess]);

  const handleActivate = async () => {
    try {
      await activate();
      setShowSuccess('Gate activated!');
      refetch();
    } catch (err) {
      // Error is handled by the hook
    }
  };

  const handleToggleEbrake = async () => {
    try {
      await toggleEbrake();
      setShowSuccess('E-brake toggled!');
      refetch();
    } catch (err) {
      // Error is handled by the hook
    }
  };

  const isEbrakeActive = status?.ebrake_active === true || status?.ebrake_active === 1;
  const isDoorMoving = status?.door_motion && status.door_motion !== 'stopped';

  return (
    <main className="min-h-screen p-4 md:p-8 flex flex-col items-center justify-center">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-white">Gate Controller</h1>
          <p className="text-gray-400 text-sm">Monitor and control your gate</p>
        </div>

        {/* Error Display */}
        {(error || controlError) && (
          <div className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
            <p className="text-sm">{error || controlError}</p>
          </div>
        )}

        {/* Success Message */}
        {showSuccess && (
          <div className="bg-green-500/10 border border-green-500 text-green-400 px-4 py-3 rounded-lg">
            <p className="text-sm">{showSuccess}</p>
          </div>
        )}

        {/* Status Card */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-xl border border-white/20">
          <div className="space-y-4">
            {/* Door Status */}
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Door Status</span>
              {loading ? (
                <div className="h-6 w-20 bg-white/20 rounded animate-pulse" />
              ) : (
                <span className="text-white font-semibold capitalize">{status?.door || 'Unknown'}</span>
              )}
            </div>

            {/* Motion Status */}
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Motion</span>
              {loading ? (
                <div className="h-6 w-24 bg-white/20 rounded animate-pulse" />
              ) : (
                <div className="flex items-center gap-2">
                  {isDoorMoving && (
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                  )}
                  <span className="text-white font-semibold capitalize">
                    {status?.door_motion || 'Stopped'}
                  </span>
                </div>
              )}
            </div>

            {/* E-Brake Status */}
            <div className="flex items-center justify-between">
              <span className="text-gray-300">E-Brake</span>
              {loading ? (
                <div className="h-6 w-16 bg-white/20 rounded animate-pulse" />
              ) : (
                <span className={`font-semibold ${isEbrakeActive ? 'text-red-400' : 'text-green-400'}`}>
                  {isEbrakeActive ? 'Active' : 'Inactive'}
                </span>
              )}
            </div>

            {/* Timestamp */}
            {status?.timestamp && (
              <div className="text-xs text-gray-500 pt-2 border-t border-white/10">
                Last updated: {new Date(status.timestamp).toLocaleTimeString()}
              </div>
            )}
          </div>
        </div>

        {/* Control Buttons */}
        <div className="space-y-3">
          {/* Activate Button */}
          <button
            onClick={handleActivate}
            disabled={activating || loading || isEbrakeActive}
            className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-200 ${
              activating || loading || isEbrakeActive
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 active:scale-95 text-white shadow-lg shadow-blue-600/30'
            }`}
          >
            {activating ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Activating...
              </span>
            ) : isEbrakeActive ? (
              'E-Brake Active'
            ) : (
              '🚗 Activate Gate'
            )}
          </button>

          {/* E-Brake Toggle Button */}
          <button
            onClick={handleToggleEbrake}
            disabled={togglingEbrake || loading}
            className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-200 ${
              togglingEbrake || loading
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : isEbrakeActive
                ? 'bg-green-600 hover:bg-green-700 active:scale-95 text-white shadow-lg shadow-green-600/30'
                : 'bg-red-600 hover:bg-red-700 active:scale-95 text-white shadow-lg shadow-red-600/30'
            }`}
          >
            {togglingEbrake ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Toggling...
              </span>
            ) : isEbrakeActive ? (
              '🔓 Release E-Brake'
            ) : (
              '⚠️ Engage E-Brake'
            )}
          </button>
        </div>

        {/* Install Prompt */}
        <InstallPrompt />

        {/* Footer */}
        <div className="text-center text-xs text-gray-500 pt-4">
          <p>Gate Controller v2.0.0</p>
        </div>
      </div>
    </main>
  );
}

function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowPrompt(true);
    };

    window.addEventListener('beforeinstallprompt', handler);

    return () => {
      window.removeEventListener('beforeinstallprompt', handler);
    };
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
      setShowPrompt(false);
    }
    setDeferredPrompt(null);
  };

  if (!showPrompt) return null;

  return (
    <div className="bg-blue-500/10 border border-blue-500 rounded-lg p-4 flex items-center justify-between">
      <p className="text-sm text-blue-400">Install app for quick access</p>
      <button
        onClick={handleInstall}
        className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
      >
        Install
      </button>
    </div>
  );
}
