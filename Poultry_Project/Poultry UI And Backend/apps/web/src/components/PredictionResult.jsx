import React from 'react';
import { motion } from 'framer-motion';

const PredictionResult = ({ analysisResult }) => {
  if (!analysisResult) return null;

  const { primary_diagnosis, confidence } = analysisResult;
  const confidencePercent = Number(confidence).toFixed(1);
  
  const diagnosisKey = primary_diagnosis?.toLowerCase().replace(/ /g, '-').replace(/_/g, '-');
  
  // Map diagnosis to specific animated gradients
  let colorTheme = {
    bg: 'bg-gradient-to-r from-gray-700 via-gray-800 to-gray-900',
    text: 'text-white',
    bar: 'bg-gray-300',
    emoji: '🔍'
  };

  if (diagnosisKey === 'healthy') {
    colorTheme = {
      bg: 'bg-gradient-to-r from-emerald-500 via-teal-500 to-green-600',
      text: 'text-white',
      bar: 'bg-white',
      emoji: '✅'
    };
  } else if (diagnosisKey === 'bumblefoot') {
    colorTheme = {
      bg: 'bg-gradient-to-r from-red-500 via-rose-600 to-red-700',
      text: 'text-white',
      bar: 'bg-white',
      emoji: '⚠️'
    };
  } else if (diagnosisKey === 'fowl-pox') {
    colorTheme = {
      bg: 'bg-gradient-to-r from-orange-500 via-amber-600 to-orange-700',
      text: 'text-white',
      bar: 'bg-white',
      emoji: '⚠️'
    };
  } else if (diagnosisKey === 'infectious-coryza') {
    colorTheme = {
      bg: 'bg-gradient-to-r from-purple-500 via-fuchsia-600 to-purple-700',
      text: 'text-white',
      bar: 'bg-white',
      emoji: '⚠️'
    };
  } else if (diagnosisKey === 'crd') {
    colorTheme = {
      bg: 'bg-gradient-to-r from-blue-500 via-indigo-600 to-blue-700',
      text: 'text-white',
      bar: 'bg-white',
      emoji: '⚠️'
    };
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className={`${colorTheme.bg} bg-size-200 animate-gradient-shift rounded-3xl p-8 md:p-12 shadow-2xl w-full relative overflow-hidden border border-white/20`}
    >
      <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-black/10 rounded-full blur-3xl -ml-20 -mb-20 pointer-events-none"></div>
      
      <div className="text-center space-y-6 relative z-10">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2, type: "spring" }}
          className="text-6xl md:text-8xl drop-shadow-xl"
        >
          {colorTheme.emoji}
        </motion.div>
        
        <div>
          <h2 className="text-sm font-black text-white/90 uppercase tracking-widest mb-2 drop-shadow-md">
            Primary Diagnosis
          </h2>
          <h3 className={`text-4xl md:text-6xl font-black capitalize ${colorTheme.text} drop-shadow-[0_4px_4px_rgba(0,0,0,0.3)]`}>
            {primary_diagnosis?.replace(/_/g, ' ')}
          </h3>
        </div>
        
        <div className="max-w-md mx-auto space-y-3 pt-6">
          <div className="flex items-center justify-between">
            <span className="text-white/90 font-black text-lg drop-shadow-md">Confidence Score</span>
            <span className="text-4xl font-black text-white drop-shadow-[0_2px_2px_rgba(0,0,0,0.5)]">{confidencePercent}%</span>
          </div>
          
          <div className="relative h-5 w-full overflow-hidden rounded-full bg-black/40 shadow-inner border border-white/10">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${confidencePercent}%` }}
              transition={{ duration: 1.5, delay: 0.4, ease: "easeOut" }}
              className={`h-full ${colorTheme.bar} shadow-[0_0_15px_rgba(255,255,255,0.8)] rounded-full`}
            />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default PredictionResult;