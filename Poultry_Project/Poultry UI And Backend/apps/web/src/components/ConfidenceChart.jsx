import React from 'react';
import { motion } from 'framer-motion';

const ConfidenceChart = ({ predictions }) => {
  const sortedPredictions = [...predictions].sort((a, b) => b.confidence - a.confidence);

  const getColorForClass = (className) => {
    const key = className.toLowerCase().replace(/ /g, '-').replace(/_/g, '-');
    switch (key) {
      case 'healthy': return 'bg-disease-healthy';
      case 'bumblefoot': return 'bg-disease-bumblefoot';
      case 'fowl-pox': return 'bg-disease-fowl-pox';
      case 'infectious-coryza': return 'bg-disease-coryza';
      case 'crd': return 'bg-disease-crd';
      default: return 'bg-gray-500';
    }
  };

  const getEmojiForClass = (className) => {
    const key = className.toLowerCase().replace(/ /g, '-').replace(/_/g, '-');
    switch (key) {
      case 'healthy': return '✅';
      case 'bumblefoot': return '🦠';
      case 'fowl-pox': return '🔴';
      case 'infectious-coryza': return '⚠️';
      case 'crd': return '🟣';
      default: return '❓';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="bg-gradient-to-br from-white via-gray-50 to-white bg-size-200 animate-gradient-pulse rounded-3xl p-8 border border-gray-200 shadow-xl"
    >
      <h3 className="text-2xl font-black text-gray-900 mb-8 border-b border-gray-200 pb-4">All Predictions</h3>
      
      <div className="space-y-6">
        {sortedPredictions.map((pred, index) => {
          const barColor = getColorForClass(pred.disease);
          return (
            <motion.div
              key={pred.disease}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="space-y-2"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl drop-shadow-sm">{getEmojiForClass(pred.disease)}</span>
                  <span className="text-gray-800 font-bold capitalize text-lg">
                    {pred.disease.replace(/_/g, ' ')}
                  </span>
                </div>
                <span className="text-gray-900 font-black text-xl">{(pred.confidence * 100).toFixed(1)}%</span>
              </div>
              
              <div className="relative h-4 w-full overflow-hidden rounded-full bg-gray-200 shadow-inner">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${pred.confidence * 100}%` }}
                  transition={{ duration: 1, delay: index * 0.1, ease: "easeOut" }}
                  className={`h-full ${barColor} shadow-sm`}
                />
              </div>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  );
};

export default ConfidenceChart;