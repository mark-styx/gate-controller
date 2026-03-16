'use client';

import { useState, useEffect } from 'react';
import { gateApi } from '@/lib/api';

interface Settings {
  apiUrl: string;
  apiKey: string;
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings>({
    apiUrl: '',
    apiKey: '',
  });
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load settings from localStorage
    const savedUrl = localStorage.getItem('gate_api_url');
    const savedKey = localStorage.getItem('gate_api_key');
    
    if (savedUrl || savedKey) {
      setSettings({
        apiUrl: savedUrl || process.env.NEXT_PUBLIC_API_URL || '',
        apiKey: savedKey || process.env.NEXT_PUBLIC_API_KEY || '',
      });
    } else {
      // Use env defaults
      setSettings({
        apiUrl: process.env.NEXT_PUBLIC_API_URL || '',
        apiKey: process.env.NEXT_PUBLIC_API_KEY || '',
      });
    }
  }, []);

  const handleSave = () => {
    try {
      localStorage.setItem('gate_api_url', settings.apiUrl);
      localStorage.setItem('gate_api_key', settings.apiKey);
      
      // Update the API client
      gateApi.setBaseUrl(settings.apiUrl);
      gateApi.setApiKey(settings.apiKey);
      
      setSaved(true);
      setError(null);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setError('Failed to save settings');
    }
  };

  const handleReset = () => {
    localStorage.removeItem('gate_api_url');
    localStorage.removeItem('gate_api_key');
    setSettings({
      apiUrl: process.env.NEXT_PUBLIC_API_URL || '',
      apiKey: process.env.NEXT_PUBLIC_API_KEY || '',
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-white">Settings</h1>
          <a
            href="/"
            className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
          >
            ← Back
          </a>
        </div>

        {/* Success Message */}
        {saved && (
          <div className="bg-green-500/10 border border-green-500 text-green-400 px-4 py-3 rounded-lg">
            Settings saved successfully!
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Settings Form */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-xl border border-white/20 space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-white mb-4">API Configuration</h2>
            <p className="text-sm text-gray-400 mb-6">
              Configure the connection to your Gate Controller API. These settings override environment variables.
            </p>
          </div>

          {/* API URL */}
          <div className="space-y-2">
            <label htmlFor="apiUrl" className="block text-sm font-medium text-gray-300">
              API URL
            </label>
            <input
              id="apiUrl"
              type="url"
              value={settings.apiUrl}
              onChange={(e) => setSettings({ ...settings, apiUrl: e.target.value })}
              placeholder="http://your-pi-ip:8000"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-gray-500">
              The URL where your Gate Controller API is running
            </p>
          </div>

          {/* API Key */}
          <div className="space-y-2">
            <label htmlFor="apiKey" className="block text-sm font-medium text-gray-300">
              API Key
            </label>
            <input
              id="apiKey"
              type="password"
              value={settings.apiKey}
              onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
              placeholder="your-api-key"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
            />
            <p className="text-xs text-gray-500">
              Your API key from gate_control/config.py
            </p>
          </div>

          {/* Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSave}
              className="flex-1 py-3 px-6 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition-colors"
            >
              Save Settings
            </button>
            <button
              onClick={handleReset}
              className="py-3 px-6 bg-gray-600 hover:bg-gray-700 rounded-lg text-white font-semibold transition-colors"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Info Box */}
        <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
          <h3 className="text-blue-400 font-semibold mb-2">ℹ️ How to find your settings</h3>
          <ul className="text-sm text-gray-300 space-y-1">
            <li>• API URL: Run <code className="bg-white/10 px-1 rounded">hostname -I</code> on your Pi</li>
            <li>• API Key: Check <code className="bg-white/10 px-1 rounded">gate_control/config.py</code></li>
            <li>• Or run: <code className="bg-white/10 px-1 rounded">../gate.sh key</code></li>
          </ul>
        </div>

        {/* Security Note */}
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
          <h3 className="text-yellow-400 font-semibold mb-2">⚠️ Security Note</h3>
          <p className="text-sm text-gray-300">
            Your API key is stored locally in your browser. Never share your API key publicly.
          </p>
        </div>
      </div>
    </div>
  );
}
