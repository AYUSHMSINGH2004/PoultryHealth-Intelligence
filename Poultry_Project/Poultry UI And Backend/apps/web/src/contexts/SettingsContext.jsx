import React, { createContext, useContext, useState, useEffect } from 'react';

const SettingsContext = createContext();

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return context;
};

export const SettingsProvider = ({ children }) => {
  const sanitizeUrl = (url) => {
    if (!url || typeof url !== 'string') return 'http://127.0.0.1:8000';
    let clean = url.trim().replace(/\/+$/, '');
    if (!clean || clean.includes('0.0.0.0')) {
      clean = (clean || '').replace(/0\.0\.0\.0/g, '127.0.0.1') || 'http://127.0.0.1:8000';
    }
    return clean;
  };

  const [serverUrl, setServerUrlState] = useState(() => {
    const saved = localStorage.getItem('fastapi_server_url');
    const clean = sanitizeUrl(saved);
    try {
      localStorage.setItem('fastapi_server_url', clean);
    } catch (e) {}
    return clean;
  });
  
  const [isConnected, setIsConnected] = useState(false);
  const [isChecking, setIsChecking] = useState(false);

  const setServerUrl = (url) => {
    const clean = sanitizeUrl(url);
    try {
      localStorage.setItem('fastapi_server_url', clean);
    } catch (e) {}
    setServerUrlState(clean);
  };

  const checkConnection = async () => {
    setIsChecking(true);
    const targetUrl = sanitizeUrl(serverUrl);
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4000);
      
      const response = await fetch(`${targetUrl}/`, {
        method: 'GET',
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      setIsConnected(response.ok);
      return response.ok;
    } catch (error) {
      setIsConnected(false);
      return false;
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    const clean = sanitizeUrl(serverUrl);
    if (clean !== serverUrl) {
      setServerUrlState(clean);
    }
    try {
      localStorage.setItem('fastapi_server_url', clean);
    } catch (e) {}
    checkConnection();
  }, [serverUrl]);

  const value = {
    serverUrl,
    setServerUrl,
    isConnected,
    isChecking,
    checkConnection
  };

  return (
    <SettingsContext.Provider value={value}>
      {children}
    </SettingsContext.Provider>
  );
};