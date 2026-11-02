import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Shield, Target, Zap, Users, Eye, FileText } from 'lucide-react';
import ModelPerformance from '@/components/ModelPerformance.jsx';

const AboutPage = () => {
  return (
    <>
      <Helmet>
        <title>About - PoultryHealth Intelligence</title>
        <meta name="description" content="Learn more about PoultryHealth Intelligence: Hierarchical Deep Learning and Grounded Generative AI for Poultry Disease Diagnosis." />
      </Helmet>
      <div className="min-h-screen bg-gray-50 py-20">
        <div className="container mx-auto px-4 max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white rounded-[3rem] p-8 md:p-16 lg:p-20 shadow-2xl border border-gray-200 relative overflow-hidden mb-16"
          >
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-br from-primary/10 to-accent/10 rounded-full blur-3xl -mr-64 -mt-64 opacity-60 pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-gradient-to-tr from-secondary/10 to-blue-500/10 rounded-full blur-3xl -ml-64 -mb-64 opacity-60 pointer-events-none"></div>

            <div className="text-center mb-20 relative z-10">
              <h1 className="text-5xl md:text-7xl font-black text-gray-900 mb-8 drop-shadow-sm">About The Project</h1>
              <p className="text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed font-medium">
                Empowering poultry farmers and veterinarians with cutting-edge artificial intelligence tools to quickly and accurately diagnose common poultry diseases.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-12 mb-20 relative z-10">
              <div className="bg-gray-50 p-10 rounded-[2rem] border border-gray-200 shadow-lg hover:shadow-xl transition-all hover:-translate-y-2 group">
                <div className="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center shadow-md mb-8 group-hover:scale-110 transition-transform">
                  <Target className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-3xl font-black text-gray-900 mb-5">Our Mission</h2>
                <p className="text-gray-700 leading-relaxed text-lg font-bold">
                  Early detection is crucial for preventing outbreaks and ensuring the health and welfare of flocks. Our mission is to democratize access to expert-level veterinary diagnostics through an easy-to-use, highly accurate AI platform. By combining deep learning with generative AI, we provide not just a diagnosis, but actionable treatment plans.
                </p>
              </div>
              <div className="bg-gray-50 p-10 rounded-[2rem] border border-gray-200 shadow-lg hover:shadow-xl transition-all hover:-translate-y-2 group">
                <div className="w-16 h-16 bg-secondary rounded-2xl flex items-center justify-center shadow-md mb-8 group-hover:scale-110 transition-transform">
                  <Shield className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-3xl font-black text-gray-900 mb-5">Why It Matters</h2>
                <p className="text-gray-700 leading-relaxed text-lg font-bold">
                  Poultry diseases can devastate flocks rapidly, leading to significant economic losses and food security issues. Traditional diagnostic methods can be slow and require specialized expertise. Our system bridges this gap, offering instant, reliable insights directly in the field.
                </p>
              </div>
            </div>

            <div className="bg-gray-900 rounded-[2.5rem] p-12 md:p-16 text-white relative z-10 shadow-2xl overflow-hidden">
              <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSIvPjwvc3ZnPg==')] opacity-50"></div>
              <div className="absolute top-0 right-0 w-64 h-64 bg-primary/30 rounded-full blur-3xl -mr-32 -mt-32"></div>

              <h2 className="text-4xl font-black mb-12 text-center relative z-10 drop-shadow-md">Key Platform Features</h2>
              <div className="grid sm:grid-cols-2 gap-8 relative z-10">
                {[
                  { icon: Zap, title: "Advanced Deep Learning", desc: "State-of-the-art CNNs for high-accuracy classification.", color: "text-accent" },
                  { icon: Eye, title: "Visual Interpretability", desc: "Real-time Grad-CAM heatmaps show exactly what the AI sees.", color: "text-blue-400" },
                  { icon: FileText, title: "Comprehensive Reports", desc: "AI-generated diagnostic reports with actionable steps.", color: "text-emerald-400" },
                  { icon: Users, title: "User-Friendly Interface", desc: "Designed for quick field assessments by anyone.", color: "text-orange-400" }
                ].map((feature, idx) => (
                  <div key={idx} className="flex gap-6 bg-white/5 backdrop-blur-md p-6 rounded-3xl border border-white/10 hover:bg-white/10 transition-all hover:scale-105 group">
                    <div className="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-inner border border-white/5 group-hover:rotate-12 transition-transform">
                      <feature.icon className={`w-7 h-7 ${feature.color}`} />
                    </div>
                    <div>
                      <h4 className="font-black text-white text-xl mb-2 drop-shadow-sm">{feature.title}</h4>
                      <p className="text-gray-300 text-base leading-relaxed font-bold">{feature.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Model Performance Section */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
          >
            <ModelPerformance />
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default AboutPage;