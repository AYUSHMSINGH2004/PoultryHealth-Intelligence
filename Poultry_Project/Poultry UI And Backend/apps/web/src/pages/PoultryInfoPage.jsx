import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, AlertCircle, ShieldAlert, Wind, HeartPulse, CheckCircle, Info, Shield, Activity } from 'lucide-react';

const diseasesData = {
  'bumblefoot': {
    name: "Bumblefoot",
    icon: AlertCircle,
    color: "#EF4444", // disease-bumblefoot
    gradient: "from-red-500 via-rose-600 to-red-700",
    animation: "animate-gradient-shift",
    description: "Bumblefoot (pododermatitis) is a bacterial infection and inflammatory reaction on the feet of birds, rodents, and rabbits.",
    symptoms: ["Swelling of the foot pad", "Hard, pus-filled abscess", "Limping or lameness", "Reluctance to walk or perch", "Black or brown scab on the bottom of the foot"],
    causes: ["Rough perches or splintered wood", "Hard landings from high perches", "Poor sanitation and wet litter", "Vitamin A deficiency", "Obesity"],
    treatment: ["Soak the foot in warm water with Epsom salts", "Carefully remove the scab and clean the abscess", "Apply antibacterial ointment", "Wrap the foot with a clean bandage", "In severe cases, consult a vet for antibiotics or surgery"],
    prevention: ["Provide smooth, appropriately sized perches", "Keep litter clean and dry", "Ensure a balanced diet", "Regularly inspect birds' feet"]
  },
  'fowl-pox': {
    name: "Fowl Pox",
    icon: ShieldAlert,
    color: "#F97316", // disease-fowl-pox
    gradient: "from-orange-500 via-amber-600 to-orange-700",
    animation: "animate-gradient-shift",
    description: "Fowl pox is a relatively slow-spreading viral infection that affects most bird species. It occurs in two forms: dry (cutaneous) and wet (diphtheritic).",
    symptoms: ["Dry form: Wart-like nodules on unfeathered areas (comb, wattles, face)", "Wet form: Yellowish, cheesy lesions in the mouth and throat", "Drop in egg production", "Loss of appetite", "Respiratory distress (wet form)"],
    causes: ["Avian poxvirus", "Spread by biting insects, especially mosquitoes", "Direct contact with infected birds or contaminated environments"],
    treatment: ["No specific cure for the virus", "Provide supportive care and reduce stress", "Treat secondary bacterial infections with antibiotics if necessary", "Apply iodine or specialized ointments to dry lesions to prevent secondary infection"],
    prevention: ["Vaccination is highly effective", "Control mosquito populations", "Maintain strict biosecurity", "Quarantine new birds"]
  },
  'infectious-coryza': {
    name: "Infectious Coryza",
    icon: Wind,
    color: "#A855F7", // disease-coryza
    gradient: "from-purple-500 via-fuchsia-600 to-purple-700",
    animation: "animate-gradient-flow",
    description: "Infectious coryza is an acute respiratory disease of chickens characterized by facial swelling, nasal discharge, and sneezing.",
    symptoms: ["Swelling of the face and wattles", "Foul-smelling, thick nasal and ocular discharge", "Sneezing and difficulty breathing", "Significant drop in feed and water consumption", "Drastic reduction in egg production"],
    causes: ["Bacterium Avibacterium paragallinarum", "Spread through direct contact, airborne droplets, and contaminated drinking water"],
    treatment: ["Antibiotics (e.g., erythromycin, oxytetracycline) administered in water or feed", "Isolate infected birds immediately", "Note: Recovered birds remain carriers for life"],
    prevention: ["All-in/all-out management system", "Vaccination in endemic areas", "Strict biosecurity and sanitation", "Depopulate and thoroughly clean facilities after an outbreak"]
  },
  'crd': {
    name: "CRD (Chronic Respiratory Disease)",
    icon: HeartPulse,
    color: "#3B82F6", // disease-crd
    gradient: "from-blue-500 via-indigo-600 to-blue-700",
    animation: "animate-gradient-flow",
    description: "CRD is a common respiratory infection in poultry, primarily caused by Mycoplasma gallisepticum, often complicated by other bacteria or viruses.",
    symptoms: ["Coughing, sneezing, and snicking", "Nasal discharge and bubbly eyes", "Swollen sinuses", "Reduced feed intake and weight loss", "Poor egg production and shell quality"],
    causes: ["Mycoplasma gallisepticum (MG)", "Often triggered by stress (moving, cold drafts, poor ventilation)", "Complicated by E. coli or infectious bronchitis"],
    treatment: ["Broad-spectrum antibiotics (e.g., tylosin, tetracyclines) can reduce symptoms but do not eliminate the infection", "Improve ventilation and reduce dust/ammonia", "Provide supportive care and vitamins"],
    prevention: ["Purchase MG-free stock", "Maintain excellent ventilation and air quality", "Minimize stress", "Vaccination programs where applicable"]
  },
  'healthy': {
    name: "Healthy Poultry",
    icon: CheckCircle,
    color: "#10B981", // disease-healthy
    gradient: "from-emerald-500 via-teal-500 to-green-600",
    animation: "animate-gradient-flow",
    description: "A healthy bird is active, alert, and exhibits normal behaviors. Regular monitoring is key to maintaining flock health.",
    symptoms: ["Bright, clear eyes", "Red, plump comb and wattles (in laying hens)", "Smooth, neat plumage", "Active foraging and scratching", "Normal droppings (firm, grayish-brown with a white cap)"],
    causes: ["Excellent husbandry", "Balanced nutrition", "Clean environment", "Low stress"],
    treatment: ["N/A - Maintain current practices"],
    prevention: ["Provide clean, fresh water daily", "Feed a high-quality, age-appropriate diet", "Keep the coop clean, dry, and well-ventilated", "Practice good biosecurity", "Conduct daily health checks"]
  }
};

const PoultryInfoPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialDisease = searchParams.get('disease') || 'bumblefoot';
  const [activeTab, setActiveTab] = useState(
    diseasesData[initialDisease] ? initialDisease : 'bumblefoot'
  );

  useEffect(() => {
    const disease = searchParams.get('disease');
    if (disease && diseasesData[disease]) {
      setActiveTab(disease);
    }
  }, [searchParams]);

  const handleTabChange = (key) => {
    setActiveTab(key);
    setSearchParams({ disease: key });
  };

  const activeData = diseasesData[activeTab];
  const ActiveIcon = activeData.icon;

  return (
    <>
      <Helmet>
        <title>Poultry Information - Disease Guide</title>
        <meta name="description" content="Detailed information and guide on common poultry diseases." />
      </Helmet>
      <div className="min-h-screen bg-gray-50 py-16">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="flex items-center gap-5 mb-12">
            <div className="p-4 bg-gray-900 rounded-2xl shadow-lg">
              <BookOpen className="w-10 h-10 text-white" />
            </div>
            <div>
              <h1 className="text-4xl md:text-5xl font-black text-gray-900 tracking-tight">Disease Reference Guide</h1>
              <p className="text-gray-600 mt-2 text-lg font-medium">Comprehensive information on identification, treatment, and prevention.</p>
            </div>
          </div>

          <div className="flex flex-col lg:flex-row gap-10">
            {/* Sidebar Navigation */}
            <div className="lg:w-1/3 xl:w-1/4 flex flex-col gap-3">
              {Object.entries(diseasesData).map(([key, data]) => {
                const Icon = data.icon;
                const isActive = activeTab === key;
                return (
                  <button
                    key={key}
                    onClick={() => handleTabChange(key)}
                    className={`relative flex items-center gap-4 p-5 rounded-2xl text-left transition-all duration-300 overflow-hidden group ${
                      isActive 
                        ? `bg-gradient-to-r ${data.gradient} bg-size-200 ${data.animation} text-white shadow-xl scale-105 z-10 border border-white/20` 
                        : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200 hover:shadow-md'
                    }`}
                  >
                    {!isActive && (
                      <div 
                        className="absolute left-0 top-0 bottom-0 w-2 transition-all duration-300 group-hover:w-3"
                        style={{ backgroundColor: data.color }}
                      />
                    )}
                    <Icon className={`w-6 h-6 relative z-10 ${isActive ? 'text-white drop-shadow-md' : 'text-gray-500 group-hover:text-gray-800'}`} />
                    <span className={`font-bold text-lg relative z-10 ${isActive ? 'drop-shadow-md' : ''}`}>{data.name}</span>
                  </button>
                );
              })}
            </div>

            {/* Content Area */}
            <div className="lg:w-2/3 xl:w-3/4">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.4 }}
                  className="bg-white rounded-[2.5rem] shadow-2xl border border-gray-200 overflow-hidden"
                >
                  {/* Header */}
                  <div 
                    className={`p-10 md:p-14 text-white relative overflow-hidden bg-gradient-to-r ${activeData.gradient} bg-size-200 ${activeData.animation}`}
                  >
                    <div className="absolute top-0 right-0 opacity-20 transform translate-x-1/4 -translate-y-1/4 mix-blend-overlay">
                      <ActiveIcon className="w-96 h-96" />
                    </div>
                    <div className="relative z-10 flex items-center gap-5 mb-6">
                      <div className="p-4 bg-white/20 rounded-2xl backdrop-blur-md shadow-inner border border-white/20">
                        <ActiveIcon className="w-10 h-10 text-white drop-shadow-md" />
                      </div>
                      <h2 className="text-4xl md:text-5xl font-black drop-shadow-lg">{activeData.name}</h2>
                    </div>
                    <p className="text-white/95 text-xl max-w-3xl relative z-10 leading-relaxed font-medium drop-shadow-md">
                      {activeData.description}
                    </p>
                  </div>

                  {/* Details */}
                  <div className="p-10 md:p-14 space-y-10">
                    <div className="grid md:grid-cols-2 gap-10">
                      <div className="bg-gray-50 p-8 rounded-3xl border border-gray-200 hover:shadow-lg transition-shadow relative overflow-hidden group">
                        <div className="absolute left-0 top-0 bottom-0 w-2" style={{ backgroundColor: activeData.color }}></div>
                        <h3 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                          <Activity className="w-6 h-6" style={{ color: activeData.color }} />
                          Common Symptoms
                        </h3>
                        <ul className="space-y-4">
                          {activeData.symptoms.map((item, i) => (
                            <li key={i} className="flex items-start gap-3 text-gray-800 font-bold">
                              <span className="mt-1.5 w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: activeData.color }}></span>
                              <span>{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-gray-50 p-8 rounded-3xl border border-gray-200 hover:shadow-lg transition-shadow relative overflow-hidden group">
                        <div className="absolute left-0 top-0 bottom-0 w-2" style={{ backgroundColor: activeData.color }}></div>
                        <h3 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                          <Info className="w-6 h-6" style={{ color: activeData.color }} />
                          Primary Causes
                        </h3>
                        <ul className="space-y-4">
                          {activeData.causes.map((item, i) => (
                            <li key={i} className="flex items-start gap-3 text-gray-800 font-bold">
                              <span className="mt-1.5 w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: activeData.color }}></span>
                              <span>{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="bg-white p-8 rounded-3xl border-2 border-gray-200 shadow-md hover:shadow-xl transition-shadow">
                      <h3 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                        <Shield className="w-7 h-7" style={{ color: activeData.color }} />
                        Treatment & Management
                      </h3>
                      <ul className="space-y-4">
                        {activeData.treatment.map((item, i) => (
                          <li key={i} className="flex items-start gap-4 text-gray-900 bg-gray-50 p-4 rounded-xl font-bold border border-gray-100">
                            <CheckCircle className="w-6 h-6 flex-shrink-0 mt-0.5" style={{ color: activeData.color }} />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="p-8 rounded-3xl border-2 relative overflow-hidden" style={{ borderColor: `${activeData.color}40`, backgroundColor: `${activeData.color}05` }}>
                      <h3 className="text-2xl font-black mb-6 flex items-center gap-3" style={{ color: activeData.color }}>
                        <ShieldAlert className="w-7 h-7" />
                        Prevention Strategies
                      </h3>
                      <div className="grid sm:grid-cols-2 gap-4">
                        {activeData.prevention.map((item, i) => (
                          <div key={i} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm text-gray-900 font-black flex items-center gap-3 hover:scale-[1.02] transition-transform">
                            <div className="w-3 h-3 rounded-full shadow-sm" style={{ backgroundColor: activeData.color }}></div>
                            {item}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default PoultryInfoPage;