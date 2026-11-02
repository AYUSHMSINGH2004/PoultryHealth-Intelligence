import React from 'react';
import { motion } from 'framer-motion';

const diseaseInfo = {
  healthy: {
    emoji: '✅',
    title: 'Healthy',
    description: 'No disease detected. The poultry appears to be in good health with no visible signs of illness.',
    actions: 'Continue regular monitoring and maintain good hygiene practices. Ensure proper nutrition and clean water supply.'
  },
  coccidiosis: {
    emoji: '🦠',
    title: 'Coccidiosis',
    description: 'A parasitic disease affecting the intestinal tract, causing bloody diarrhea, poor growth, and weakness in birds.',
    actions: 'Isolate affected birds immediately. Administer anticoccidial medication as prescribed. Improve sanitation and reduce overcrowding. Consult a veterinarian for treatment plan.'
  },
  salmonella: {
    emoji: '🔴',
    title: 'Salmonella',
    description: 'Bacterial infection causing severe diarrhea, dehydration, and potential death, especially in young birds. Highly contagious.',
    actions: 'Quarantine infected birds immediately. Administer antibiotic treatment under veterinary supervision. Enhance biosecurity measures and disinfect facilities thoroughly.'
  },
  newcastle: {
    emoji: '⚠️',
    title: 'Newcastle Disease',
    description: 'Highly contagious viral disease affecting respiratory, nervous, and digestive systems. Can cause high mortality rates in unvaccinated flocks.',
    actions: 'URGENT: Immediate isolation required. Vaccinate all healthy birds. Contact veterinary authorities immediately. This is a reportable disease in many regions.'
  },
  avian_pox: {
    emoji: '🟣',
    title: 'Avian Pox',
    description: 'Viral disease causing characteristic lesions on skin and mucous membranes. Spread by mosquitoes and direct contact.',
    actions: 'Isolate affected birds. Provide supportive care and maintain good nutrition. Vaccinate the flock. Control mosquito populations in the area.'
  }
};

const DiseaseInfoCard = ({ disease }) => {
  const info = diseaseInfo[disease] || diseaseInfo.healthy;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-purple-300/20 shadow-xl"
    >
      <div className="flex items-center gap-3 mb-4">
        <span className="text-4xl">{info.emoji}</span>
        <h3 className="text-2xl font-bold text-white">{info.title}</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-semibold text-purple-300 mb-2">Description</h4>
          <p className="text-gray-200 leading-relaxed">{info.description}</p>
        </div>
        
        <div>
          <h4 className="text-sm font-semibold text-purple-300 mb-2">Recommended Actions</h4>
          <p className="text-gray-200 leading-relaxed">{info.actions}</p>
        </div>
      </div>
    </motion.div>
  );
};

export default DiseaseInfoCard;