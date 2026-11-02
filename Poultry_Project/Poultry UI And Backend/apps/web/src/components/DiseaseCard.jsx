import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const DiseaseCard = ({ name, description, icon: Icon, color, slug }) => {
  return (
    <Link to={`/poultry-info?disease=${slug}`} className="block h-full">
      <motion.div
        whileHover={{ y: -8, scale: 1.02 }}
        className="relative rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden h-full flex flex-col bg-white border border-gray-100 group"
      >
        {/* Colored Left Border */}
        <div 
          className="absolute left-0 top-0 bottom-0 w-2 z-10 transition-all duration-300 group-hover:w-full group-hover:opacity-10"
          style={{ backgroundColor: color }}
        />
        
        <div 
          className="h-32 flex items-center justify-center relative overflow-hidden"
          style={{ backgroundColor: `${color}20` }} // 20% opacity background
        >
          <Icon 
            className="w-14 h-14 relative z-10 drop-shadow-sm group-hover:scale-110 transition-transform duration-300" 
            style={{ color: color }}
          />
        </div>
        
        <div className="p-6 flex-grow flex flex-col pl-8 relative z-20">
          <h3 className="text-xl font-black text-gray-900 mb-3 group-hover:text-gray-900 transition-colors">{name}</h3>
          <p className="text-gray-600 text-sm flex-grow leading-relaxed font-medium">{description}</p>
          <div 
            className="mt-5 text-sm font-bold flex items-center gap-2 opacity-90 group-hover:opacity-100 transition-opacity" 
            style={{ color }}
          >
            Learn more 
            <span className="group-hover:translate-x-1 transition-transform inline-block">&rarr;</span>
          </div>
        </div>
      </motion.div>
    </Link>
  );
};

export default DiseaseCard;