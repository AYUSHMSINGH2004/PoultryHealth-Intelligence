import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Activity, CheckCircle2, AlertTriangle, TrendingUp, Target, ShieldCheck } from 'lucide-react';

const MetricBar = ({ label, precision, recall }) => (
  <div className="mb-4">
    <div className="flex justify-between text-sm font-bold mb-1.5">
      <span className="text-white/90">{label}</span>
      <div className="flex gap-3 text-xs">
        <span className="text-white font-black drop-shadow-md">P: {precision}%</span>
        <span className="text-white/90 font-bold drop-shadow-md">R: {recall}%</span>
      </div>
    </div>
    <div className="space-y-2">
      <div className="h-2.5 w-full bg-black/30 rounded-full overflow-hidden flex shadow-inner border border-white/5">
        <motion.div 
          initial={{ width: 0 }}
          whileInView={{ width: `${precision}%` }}
          viewport={{ once: true }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="h-full bg-white rounded-full shadow-[0_0_10px_rgba(255,255,255,0.9)]"
        />
      </div>
      <div className="h-2.5 w-full bg-black/30 rounded-full overflow-hidden flex shadow-inner border border-white/5">
        <motion.div 
          initial={{ width: 0 }}
          whileInView={{ width: `${recall}%` }}
          viewport={{ once: true }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
          className="h-full bg-white/70 rounded-full shadow-[0_0_5px_rgba(255,255,255,0.5)]"
        />
      </div>
    </div>
  </div>
);

const StatCard = ({ title, value, icon: Icon }) => (
  <div className="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-xl flex items-center gap-4 hover:bg-white/20 transition-colors">
    <div className="p-3 rounded-xl bg-white/20 shadow-inner border border-white/10">
      <Icon className="w-7 h-7 text-white drop-shadow-md" />
    </div>
    <div>
      <p className="text-sm font-bold text-white/90">{title}</p>
      <p className="text-3xl font-black text-white drop-shadow-lg">{value}</p>
    </div>
  </div>
);

const ModelPerformance = () => {
  return (
    <div className="w-full space-y-12">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-black text-gray-900 mb-4">Model Performance & Evaluation</h2>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto font-medium">
          Our system utilizes a dual-model architecture to ensure high reliability. "The Bouncer" first determines if a bird is healthy or sick, and "The Doctor" classifies the specific disease.
        </p>
      </div>

      {/* Models Grid */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* The Doctor Model */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 bg-size-200 animate-gradient-shift rounded-[2.5rem] p-8 md:p-10 border border-white/20 shadow-2xl relative overflow-hidden text-white"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
          
          <div className="flex items-center gap-4 mb-10 relative z-10">
            <div className="p-4 bg-white/20 backdrop-blur-md rounded-2xl shadow-inner border border-white/20">
              <Activity className="w-8 h-8 text-white drop-shadow-md" />
            </div>
            <h3 className="text-3xl font-black drop-shadow-lg">The Doctor Model</h3>
            <span className="ml-auto text-xs font-black px-4 py-2 bg-white/20 backdrop-blur-md rounded-full border border-white/20 shadow-sm">4-Disease Classification</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-10 relative z-10">
            <StatCard title="Overall Accuracy" value="72%" icon={Target} />
            <div className="space-y-3">
              <div className="flex justify-between items-center text-sm font-bold bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 shadow-lg">
                <span className="text-white/90">Macro Precision</span>
                <span className="text-xl text-white font-black drop-shadow-md">70%</span>
              </div>
              <div className="flex justify-between items-center text-sm font-bold bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 shadow-lg">
                <span className="text-white/90">Macro Recall</span>
                <span className="text-xl text-white font-black drop-shadow-md">66%</span>
              </div>
            </div>
          </div>

          <div className="space-y-6 relative z-10 bg-black/10 p-6 rounded-3xl border border-white/10 backdrop-blur-sm">
            <h4 className="font-black text-xl text-white border-b border-white/20 pb-3 drop-shadow-md">Per-Disease Breakdown</h4>
            <div className="flex items-center gap-6 text-sm font-bold text-white/80 mb-4">
              <div className="flex items-center gap-2"><div className="w-4 h-4 bg-white rounded-md shadow-[0_0_8px_rgba(255,255,255,0.8)]"></div> Precision</div>
              <div className="flex items-center gap-2"><div className="w-4 h-4 bg-white/60 rounded-md"></div> Recall</div>
            </div>
            <MetricBar label="Bumblefoot" precision={80} recall={35} />
            <MetricBar label="CRD" precision={80} recall={82} />
            <MetricBar label="Fowl Pox" precision={53} recall={90} />
            <MetricBar label="Infectious Coryza" precision={67} recall={59} />
          </div>
        </motion.div>

        {/* The Bouncer Model */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-teal-500 via-emerald-600 to-green-700 bg-size-200 animate-gradient-flow rounded-[2.5rem] p-8 md:p-10 border border-white/20 shadow-2xl relative overflow-hidden text-white"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
          
          <div className="flex items-center gap-4 mb-10 relative z-10">
            <div className="p-4 bg-white/20 backdrop-blur-md rounded-2xl shadow-inner border border-white/20">
              <ShieldCheck className="w-8 h-8 text-white drop-shadow-md" />
            </div>
            <h3 className="text-3xl font-black drop-shadow-lg">The Bouncer Model</h3>
            <span className="ml-auto text-xs font-black px-4 py-2 bg-white/20 backdrop-blur-md rounded-full border border-white/20 shadow-sm">Healthy vs Sick</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-10 relative z-10">
            <StatCard title="Overall Accuracy" value="82%" icon={CheckCircle2} />
            <div className="space-y-3">
              <div className="flex justify-between items-center text-sm font-bold bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 shadow-lg">
                <span className="text-white/90">Macro Precision</span>
                <span className="text-xl text-white font-black drop-shadow-md">80%</span>
              </div>
              <div className="flex justify-between items-center text-sm font-bold bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 shadow-lg">
                <span className="text-white/90">Macro Recall</span>
                <span className="text-xl text-white font-black drop-shadow-md">82%</span>
              </div>
            </div>
          </div>

          <div className="space-y-6 relative z-10 bg-black/10 p-6 rounded-3xl border border-white/10 backdrop-blur-sm">
            <h4 className="font-black text-xl text-white border-b border-white/20 pb-3 drop-shadow-md">Condition Breakdown</h4>
            <div className="flex items-center gap-6 text-sm font-bold text-white/80 mb-4">
              <div className="flex items-center gap-2"><div className="w-4 h-4 bg-white rounded-md shadow-[0_0_8px_rgba(255,255,255,0.8)]"></div> Precision</div>
              <div className="flex items-center gap-2"><div className="w-4 h-4 bg-white/60 rounded-md"></div> Recall</div>
            </div>
            <MetricBar label="Healthy" precision={70} recall={83} />
            <MetricBar label="Sick" precision={90} recall={82} />
          </div>

          {/* Insights Callouts */}
          <div className="mt-8 space-y-4 relative z-10">
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-5 rounded-2xl flex gap-4 items-start shadow-lg hover:bg-white/20 transition-colors">
              <TrendingUp className="w-6 h-6 text-white flex-shrink-0 mt-0.5 drop-shadow-md" />
              <p className="text-base text-white font-medium leading-relaxed">
                <strong className="font-black drop-shadow-sm">Insight:</strong> CRD detection shows strong performance with 82% recall, effectively identifying the majority of true positive cases.
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-5 rounded-2xl flex gap-4 items-start shadow-lg hover:bg-white/20 transition-colors">
              <AlertTriangle className="w-6 h-6 text-white flex-shrink-0 mt-0.5 drop-shadow-md" />
              <p className="text-base text-white font-medium leading-relaxed">
                <strong className="font-black drop-shadow-sm">Insight:</strong> Fowl Pox detection achieves 90% recall, identifying most affected birds, though with lower precision (53%) indicating some false positives.
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Visualizations Section */}
      <div className="mt-20 space-y-12">
        <div className="text-center">
          <h3 className="text-3xl font-black text-gray-900 mb-4 flex items-center justify-center gap-3">
            <BarChart3 className="w-8 h-8 text-primary" />
            Evaluation Visualizations
          </h3>
        </div>

        {/* Confusion Matrices */}
        <div className="grid md:grid-cols-2 gap-8">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="bg-white p-8 rounded-[2.5rem] border border-gray-200 shadow-xl hover:shadow-2xl transition-shadow"
          >
            <h4 className="text-2xl font-black text-center mb-6 text-gray-900">The Doctor: Confusion Matrix</h4>
            <div className="rounded-2xl overflow-hidden border border-gray-200 bg-gray-50 flex items-center justify-center p-4 shadow-inner">
              <img 
                src="/images/doctor_confusion_matrix.png" 
                alt="The Doctor Model Confusion Matrix showing 4-disease classification performance" 
                className="w-full h-auto max-h-[420px] object-contain rounded-xl"
              />
            </div>
            <p className="text-base text-gray-600 mt-6 text-center font-bold leading-relaxed">
              Visualizes the true vs. predicted classifications for the 4 specific poultry diseases, highlighting areas of strong detection and common misclassifications.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="bg-white p-8 rounded-[2.5rem] border border-gray-200 shadow-xl hover:shadow-2xl transition-shadow"
          >
            <h4 className="text-2xl font-black text-center mb-6 text-gray-900">The Bouncer: Confusion Matrix</h4>
            <div className="rounded-2xl overflow-hidden border border-gray-200 bg-gray-50 flex items-center justify-center p-4 shadow-inner">
              <img 
                src="/images/bouncer_confusion_matrix.png" 
                alt="The Bouncer Model Confusion Matrix showing healthy vs sick classification" 
                className="w-full h-auto max-h-[420px] object-contain rounded-xl"
              />
            </div>
            <p className="text-base text-gray-600 mt-6 text-center font-bold leading-relaxed">
              Demonstrates the binary classification performance, showing high accuracy in distinguishing between healthy and sick poultry subjects.
            </p>
          </motion.div>
        </div>

        {/* Confidence Distribution */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-white p-10 rounded-[3rem] border border-gray-200 shadow-2xl max-w-5xl mx-auto"
        >
          <h4 className="text-3xl font-black text-center mb-8 text-gray-900">Prediction Confidence Distribution</h4>
          <div className="rounded-3xl overflow-hidden border border-gray-200 bg-gray-50 flex items-center justify-center p-6 mb-8 shadow-inner">
            <img 
              src="/images/confidence_distribution.png" 
              alt="Histogram and KDE plot showing the distribution of model prediction confidence scores" 
              className="w-full max-w-3xl h-auto object-contain rounded-xl"
            />
          </div>
          <div className="bg-gradient-to-r from-primary/10 via-secondary/10 to-primary/10 bg-size-200 animate-gradient-shift p-8 rounded-2xl border border-primary/20 shadow-sm">
            <p className="text-gray-800 font-bold text-center text-lg leading-relaxed">
              The histogram and KDE (Kernel Density Estimation) plot illustrate the distribution of confidence scores across all predictions. 
              <strong className="text-primary ml-1 font-black text-xl">Most predictions fall in the 0.6 to 0.8 confidence range.</strong> Higher scores indicate more reliable predictions, demonstrating the model's certainty when diagnosing clear symptoms.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ModelPerformance;