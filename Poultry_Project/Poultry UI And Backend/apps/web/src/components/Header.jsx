
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Settings as SettingsIcon } from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import SettingsModal from '@/components/SettingsModal.jsx';
import { useSettings } from '@/contexts/SettingsContext.jsx';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const { isConnected } = useSettings();
  const location = useLocation();

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Poultry Info', path: '/poultry-info' },
    { name: 'Predict', path: '/predict' },
  ];

  return (
    <>
      <header className="sticky top-0 z-50 w-full bg-white/95 backdrop-blur-lg border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 h-20 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="text-3xl bg-gradient-to-br from-primary to-secondary p-2 rounded-xl shadow-md group-hover:shadow-lg group-hover:scale-105 transition-all duration-300">🐔</div>
            <div>
              <h1 className="text-xl font-extrabold text-gray-900 leading-tight tracking-wide group-hover:text-primary transition-colors">PoultryHealth</h1>
              <p className="text-xs text-primary font-bold uppercase tracking-wider">Intelligence AI</p>
            </div>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            <nav className="flex items-center gap-8">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`text-sm font-bold transition-all duration-300 relative py-2 ${
                      isActive 
                        ? 'text-primary' 
                        : 'text-gray-600 hover:text-primary'
                    }`}
                  >
                    {item.name}
                    {isActive && (
                      <motion.div 
                        layoutId="activeNav"
                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-full"
                      />
                    )}
                  </Link>
                );
              })}
            </nav>

            <Button
              variant="outline"
              size="sm"
              onClick={() => setSettingsOpen(true)}
              className="flex items-center gap-2 rounded-xl border-gray-300 hover:border-primary text-gray-700 hover:text-primary transition-all text-xs font-semibold px-3 py-1.5 shadow-sm"
              title="Configure FastAPI Backend URL"
            >
              <SettingsIcon className="w-3.5 h-3.5" />
              <span>Settings</span>
              <span 
                className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500 shadow-[0_0_6px_rgba(16,185,129,0.7)]' : 'bg-red-400'}`} 
                title={isConnected ? "Backend connected" : "Backend disconnected"}
              />
            </Button>
          </div>

          {/* Mobile Menu Toggle */}
          <div className="flex md:hidden items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSettingsOpen(true)}
              className="p-2 text-gray-600"
              title="Settings"
            >
              <SettingsIcon className="w-5 h-5" />
            </Button>
            <button
              className="p-2 text-gray-600 hover:text-primary hover:bg-gray-100 rounded-md transition-colors"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

      {/* Mobile Nav */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden bg-white border-t border-gray-100 overflow-hidden shadow-xl"
          >
            <div className="flex flex-col px-4 py-4 space-y-2">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`text-base font-bold px-4 py-3 rounded-xl transition-colors ${
                      isActive 
                        ? 'bg-primary/10 text-primary' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-primary'
                    }`}
                  >
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
    <SettingsModal open={settingsOpen} onOpenChange={setSettingsOpen} />
  </>
  );
};

export default Header;
