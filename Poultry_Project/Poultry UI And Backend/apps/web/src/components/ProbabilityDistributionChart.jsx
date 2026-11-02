import React from 'react';
import { motion } from 'framer-motion';

const ProbabilityDistributionChart = ({ distribution }) => {
  if (!distribution) return null;

  const sortedDistribution = Object.entries(distribution)
    .sort((a, b) => b[1] - a[1])
    .map(([className, probability]) => ({
      className,
      probability,
      percentage: Number(probability).toFixed(1)
    }));

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

  const getTextColorForClass = (className) => {
    const key = className.toLowerCase().replace(/ /g, '-').replace(/_/g, '-');
    switch (key) {
      case 'healthy': return 'text-disease-healthy';
      case 'bumblefoot': return 'text-disease-bumblefoot';
      case 'fowl-pox': return 'text-disease-fowl-pox';
      case 'infectious-coryza': return 'text-disease-coryza';
      case 'crd': return 'text-disease-crd';
      default: return 'text-gray-700';
    }
  };

  return (
    <div className="bg-gradient-to-br from-white via-gray-50 to-white bg-size-200 animate-gradient-flow rounded-3xl p-8 w-full h-full flex flex-col shadow-inner">
      <h3 className="text-2xl font-black text-gray-900 mb-8 border-b border-gray-200 pb-4">Probability Distribution</h3>
      
      <div className="space-y-6 flex-grow overflow-y-auto pr-4 custom-scrollbar">
        {sortedDistribution.map((item, index) => {
          const barColor = getColorForClass(item.className);
          const textColor = getTextColorForClass(item.className);

          return (
            <motion.div
              key={item.className}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="relative"
            >
              <div className="flex justify-between items-end mb-2">
                <span className="text-base font-bold text-gray-800 capitalize">
                  {item.className.replace(/_/g, ' ')}
                </span>
                <span className={`text-lg font-black ${textColor} drop-shadow-sm`}>
                  {item.percentage}%
                </span>
              </div>
              
              <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden shadow-inner">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${item.percentage}%` }}
                  transition={{ duration: 1, delay: 0.2 + index * 0.1, ease: "easeOut" }}
                  className={`h-full rounded-full ${barColor} shadow-sm`}
                />
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default ProbabilityDistributionChart;