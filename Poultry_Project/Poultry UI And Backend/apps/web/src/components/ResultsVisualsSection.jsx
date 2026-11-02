import React from 'react';
import { motion } from 'framer-motion';

const ResultsVisualsSection = ({ originalImageBase64, heatmapImageBase64 }) => {
  if (!originalImageBase64 && !heatmapImageBase64) return null;

  const renderImage = (base64, label, delay) => {
    if (!base64) return null;
    
    const imageSrc = base64.startsWith('data:image') 
      ? base64 
      : `data:image/jpeg;base64,${base64}`;

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay }}
        className="flex-1 flex flex-col space-y-3"
      >
        <h4 className="text-center text-sm font-bold text-gray-700 uppercase tracking-wider">
          {label}
        </h4>
        <div className="relative rounded-xl overflow-hidden border-2 border-gray-200 shadow-md bg-gray-50 aspect-square flex items-center justify-center group">
          <img 
            src={imageSrc} 
            alt={label} 
            className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-500"
          />
        </div>
      </motion.div>
    );
  };

  return (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 w-full h-full flex flex-col">
      <h3 className="text-xl font-black text-gray-900 mb-6 border-b border-gray-200 pb-4">Analysis Visuals</h3>
      <div className="flex flex-col md:flex-row gap-6 w-full flex-grow items-center justify-center">
        {renderImage(originalImageBase64, 'Original Image', 0.1)}
        {renderImage(heatmapImageBase64, 'Grad-CAM Heatmap', 0.3)}
      </div>
    </div>
  );
};

export default ResultsVisualsSection;