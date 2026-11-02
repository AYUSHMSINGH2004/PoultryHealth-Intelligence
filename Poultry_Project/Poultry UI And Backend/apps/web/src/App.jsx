
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster.jsx';
import Header from '@/components/Header.jsx';
import HomePage from '@/pages/HomePage.jsx';
import PredictPage from '@/pages/PredictPage.jsx';
import AboutPage from '@/pages/AboutPage.jsx';
import PoultryInfoPage from '@/pages/PoultryInfoPage.jsx';
import { SettingsProvider } from '@/contexts/SettingsContext.jsx';

function App() {
  return (
    <BrowserRouter>
      <SettingsProvider>
        <div className="min-h-screen bg-background flex flex-col font-sans text-foreground selection:bg-primary selection:text-white">
          <Header />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/predict" element={<PredictPage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/poultry-info" element={<PoultryInfoPage />} />
            </Routes>
          </main>
          <Toaster />
        </div>
      </SettingsProvider>
    </BrowserRouter>
  );
}

export default App;
