import React from 'react';
import { AlertCircle, X } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { motion, AnimatePresence } from 'framer-motion';

const ErrorAlert = ({ message, onDismiss }) => {
  if (!message) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className="mb-6 relative z-50"
      >
        <Alert className="bg-red-950 border-2 border-red-600 text-white shadow-2xl p-4 rounded-lg">
          <AlertCircle className="h-6 w-6 text-red-400" />
          <AlertTitle className="text-white font-bold text-lg ml-3">Analysis Error</AlertTitle>
          <AlertDescription className="ml-3 mt-2 text-red-100 text-base">
            {message}
          </AlertDescription>
          {onDismiss && (
            <button
              onClick={onDismiss}
              className="absolute top-4 right-4 p-1.5 rounded-md bg-red-900/50 hover:bg-red-800 text-red-200 hover:text-white transition-colors"
              aria-label="Close alert"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </Alert>
      </motion.div>
    </AnimatePresence>
  );
};

export default ErrorAlert;