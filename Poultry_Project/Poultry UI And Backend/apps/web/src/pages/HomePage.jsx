import React from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button.jsx';
import { Brain, Network, Eye, Sparkles, CheckCircle2, ArrowRight, ShieldCheck, Activity, AlertCircle, ShieldAlert, HeartPulse, Wind, CheckCircle } from 'lucide-react';
import DiseaseCard from '@/components/DiseaseCard.jsx';
import CallToAction from '@/components/CallToAction.jsx';

const HomePage = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  const diseases = [
    { name: 'Bumblefoot', description: 'Bacterial infection and inflammatory reaction on the feet of birds.', icon: AlertCircle, color: '#EF4444', slug: 'bumblefoot' },
    { name: 'Fowl Pox', description: 'Viral disease causing lesions on unfeathered skin or mucous membranes.', icon: ShieldAlert, color: '#F97316', slug: 'fowl-pox' },
    { name: 'Infectious Coryza', description: 'Acute respiratory disease causing facial swelling and nasal discharge.', icon: Wind, color: '#A855F7', slug: 'infectious-coryza' },
    { name: 'CRD', description: 'Chronic Respiratory Disease, often caused by Mycoplasma gallisepticum.', icon: HeartPulse, color: '#3B82F6', slug: 'crd' },
    { name: 'Healthy', description: 'Normal, healthy poultry with no visible signs of disease.', icon: CheckCircle, color: '#10B981', slug: 'healthy' },
  ];

  return (
    <>
      <Helmet>
        <title>Home - Poultry Disease Detection System</title>
        <meta name="description" content="AI-Powered Poultry Disease Detection System" />
      </Helmet>

      {/* Hero Section - Animated Purple/Indigo/Blue Gradient */}
      <section className="relative pt-28 pb-36 overflow-hidden bg-gradient-to-r from-primary via-secondary to-blue-600 bg-size-200 animate-gradient-shift">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSIvPjwvc3ZnPg==')] opacity-50"></div>
        <div className="absolute top-0 left-0 w-full h-full bg-black/10"></div>
        
        <div className="container relative z-10 mx-auto px-4 text-center max-w-5xl">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-white/20 text-white font-bold text-sm mb-10 backdrop-blur-md border border-white/30 shadow-xl"
          >
            <Sparkles className="w-4 h-4 text-pink-300" />
            <span>Next-Generation Veterinary AI</span>
          </motion.div>

          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl md:text-7xl lg:text-8xl font-black text-white mb-8 tracking-tight leading-tight drop-shadow-2xl"
          >
            AI-Powered Poultry <br className="hidden md:block" /> 
            <span className="text-pink-300 drop-shadow-lg">Disease Detection</span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl md:text-2xl text-white/90 mb-12 max-w-3xl mx-auto leading-relaxed font-medium drop-shadow-md"
          >
            Empowering farmers and veterinarians with advanced deep learning to quickly and accurately diagnose common poultry diseases.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6"
          >
            <Button asChild size="lg" className="bg-white text-primary hover:bg-gray-100 px-10 py-7 text-xl rounded-full w-full sm:w-auto shadow-2xl transition-all hover:scale-105 font-black border-2 border-white">
              <Link to="/predict">
                Try Prediction
                <ArrowRight className="ml-3 w-6 h-6" />
              </Link>
            </Button>
            <Button asChild size="lg" className="bg-transparent text-white hover:bg-white/10 px-10 py-7 text-xl rounded-full w-full sm:w-auto shadow-xl transition-all hover:scale-105 font-bold border-2 border-white/50 hover:border-white">
              <Link to="/poultry-info">Learn More</Link>
            </Button>
          </motion.div>
        </div>
      </section>

      {/* Diseases Covered Section - Animated Indigo/Blue/Teal Gradient */}
      <section className="py-24 bg-gradient-to-r from-secondary via-blue-600 to-teal-600 bg-size-200 animate-gradient-flow relative">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="container mx-auto px-4 max-w-7xl relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-sm font-black text-teal-200 tracking-widest uppercase mb-3 drop-shadow-sm">Diagnostic Capabilities</h2>
            <h3 className="text-4xl md:text-5xl font-black text-white drop-shadow-lg">Diseases Covered</h3>
            <p className="text-blue-100 mt-5 max-w-2xl mx-auto text-lg font-medium drop-shadow-sm">Our AI model is trained to identify key conditions affecting poultry health with high accuracy.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
            {diseases.map((disease, idx) => (
              <DiseaseCard key={idx} {...disease} />
            ))}
          </div>
        </div>
      </section>

      {/* Features Section - Animated Blue/Cyan/Green Gradient */}
      <section className="py-24 bg-gradient-to-r from-blue-700 via-cyan-700 to-emerald-700 bg-size-200 animate-gradient-flow relative">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSIvPjwvc3ZnPg==')] opacity-30"></div>
        <div className="container mx-auto px-4 max-w-6xl relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-sm font-black text-cyan-300 tracking-widest uppercase mb-3 drop-shadow-sm">Core Technology</h2>
            <h3 className="text-4xl md:text-5xl font-black text-white drop-shadow-lg">Advanced Deep Learning Architecture</h3>
          </div>
          
          <motion.div 
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          >
            {[
              {
                icon: Brain,
                title: "CNN Architecture",
                desc: "Foundational deep learning for image feature extraction, automatically learning spatial hierarchies.",
                color: "text-blue-300",
                bg: "bg-blue-900/50"
              },
              {
                icon: Network,
                title: "Transfer Learning",
                desc: "Utilizing ResNet & EfficientNet for high accuracy with optimized scaling and residual connections.",
                color: "text-cyan-300",
                bg: "bg-cyan-900/50"
              },
              {
                icon: Eye,
                title: "Grad-CAM Vision",
                desc: "Visualizes which regions of the image influenced predictions, improving model interpretability.",
                color: "text-emerald-300",
                bg: "bg-emerald-900/50"
              },
              {
                icon: Sparkles,
                title: "Gemini 2.5 Flash",
                desc: "Advanced LLM generating professional veterinary action plans based on visual predictions.",
                color: "text-teal-300",
                bg: "bg-teal-900/50"
              }
            ].map((feature, idx) => (
              <motion.div key={idx} variants={itemVariants} className="bg-white/10 backdrop-blur-md p-8 rounded-3xl shadow-xl border border-white/20 hover:bg-white/20 transition-all duration-300 group hover:-translate-y-2">
                <div className={`w-16 h-16 ${feature.bg} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border border-white/10`}>
                  <feature.icon className={`w-8 h-8 ${feature.color}`} />
                </div>
                <h4 className="text-xl font-bold text-white mb-3 drop-shadow-sm">{feature.title}</h4>
                <p className="text-white/80 leading-relaxed text-sm font-medium">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Benefits Section - Light/Clean contrast */}
      <section className="py-24 bg-white relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl -mr-96 -mt-96 pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-secondary/5 rounded-full blur-3xl -ml-64 -mb-64 pointer-events-none"></div>
        
        <div className="container mx-auto px-4 max-w-6xl relative z-10">
          <div className="flex flex-col lg:flex-row items-center gap-16">
            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="flex-1"
            >
              <h2 className="text-sm font-black text-primary tracking-widest uppercase mb-3">Project Overview</h2>
              <h3 className="text-4xl md:text-5xl font-black text-gray-900 mb-6 leading-tight">Transforming Poultry Health with AI</h3>
              <p className="text-lg text-gray-700 leading-relaxed mb-8 font-medium">
                Our system leverages state-of-the-art computer vision and deep learning to analyze images of poultry and detect signs of common diseases. By providing rapid, accurate, and interpretable results, we aim to reduce mortality rates, improve flock welfare, and support sustainable farming practices.
              </p>
              <ul className="space-y-5 mt-8">
                {[
                  "Rapid field assessments for farmers",
                  "Clinical decision support for veterinarians",
                  "Actionable treatment recommendations",
                  "Interpretable AI with visual heatmaps"
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-4 text-gray-900 font-bold text-lg bg-gray-50 p-4 rounded-xl border border-gray-100 shadow-sm">
                    <div className="bg-primary p-2 rounded-lg">
                      <ShieldCheck className="w-5 h-5 text-white flex-shrink-0" />
                    </div>
                    {item}
                  </li>
                ))}
              </ul>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="flex-1 w-full bg-gray-900 rounded-[2.5rem] p-10 border border-gray-800 shadow-2xl relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary/30 to-secondary/30 rounded-full blur-3xl -mr-32 -mt-32"></div>
              
              <h4 className="text-2xl font-black text-white mb-8 relative z-10 flex items-center gap-3 drop-shadow-md">
                <div className="bg-secondary/20 p-3 rounded-xl border border-secondary/30">
                  <Activity className="w-7 h-7 text-secondary-foreground" />
                </div>
                Data & Training Practices
              </h4>
              <div className="space-y-4 relative z-10">
                {[
                  "Pretrained weights (ImageNet / COCO) fine-tuned on poultry dataset",
                  "Strong augmentations: rotations, flips, color jitters, random crop",
                  "Class-imbalance handling: weighted loss, focal loss, oversampling",
                  "Validation: stratified split, cross-validation for robust estimates",
                  "Metrics: High accuracy and F1 scores for classification"
                ].map((practice, index) => (
                  <div key={index} className="flex items-start gap-4 p-5 bg-white/5 rounded-2xl border border-white/10 hover:border-primary/50 hover:bg-white/10 transition-colors group backdrop-blur-sm">
                    <CheckCircle2 className="w-6 h-6 text-primary flex-shrink-0 mt-0.5 group-hover:scale-110 transition-transform" />
                    <p className="text-gray-200 text-sm font-bold leading-relaxed">{practice}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section - Animated Pink/Magenta/Purple Gradient */}
      <section className="py-24 bg-gradient-to-r from-pink-500 via-purple-500 to-secondary bg-size-200 animate-gradient-shift relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIi8+PC9zdmc+')] opacity-30"></div>
        <div className="container mx-auto px-4 text-center relative z-10">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-black text-white mb-6 drop-shadow-lg"
          >
            Ready to safeguard your flock?
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-pink-100 text-xl mb-10 max-w-2xl mx-auto font-medium drop-shadow-md"
          >
            Start using our AI-powered diagnostic tool today for early detection and better poultry health management.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <Button asChild size="lg" className="bg-white text-accent hover:bg-gray-50 px-12 py-7 text-xl rounded-full shadow-2xl transition-all hover:scale-105 font-black border-2 border-white">
              <Link to="/predict">Start Analysis Now</Link>
            </Button>
          </motion.div>
        </div>
      </section>
    </>
  );
};

export default HomePage;