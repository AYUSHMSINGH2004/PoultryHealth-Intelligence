import React from 'react';
import { motion } from 'framer-motion';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16 space-y-6">
      <motion.div
        className="w-20 h-20 border-4 border-primary/30 border-t-primary rounded-full shadow-[0_0_15px_rgba(124,58,237,0.5)]"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      />
      <motion.div
        className="bg-slate-900/80 backdrop-blur-md px-8 py-4 rounded-full shadow-2xl border border-white/10"
        initial={{ opacity: 0.5, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, repeat: Infinity, repeatType: "reverse" }}
      >
        <p className="text-xl text-white font-black tracking-wide drop-shadow-[0_2px_2px_rgba(0,0,0,0.8)]">
          Analyzing image... Please wait
        </p>
      </motion.div>
    </div>
  );
};

export default LoadingSpinner;