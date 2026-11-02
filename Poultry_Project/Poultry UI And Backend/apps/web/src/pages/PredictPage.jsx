
import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import { motion, AnimatePresence } from 'framer-motion';
import { useToast } from '@/components/ui/use-toast.js';
import { Button } from '@/components/ui/button';
import ImageUpload from '@/components/ImageUpload.jsx';
import LoadingSpinner from '@/components/LoadingSpinner.jsx';
import PredictionResult from '@/components/PredictionResult.jsx';
import ProbabilityDistributionChart from '@/components/ProbabilityDistributionChart.jsx';
import ResultsVisualsSection from '@/components/ResultsVisualsSection.jsx';
import MarkdownRenderer from '@/components/MarkdownRenderer.jsx';
import ErrorAlert from '@/components/ErrorAlert.jsx';
import { RefreshCw, Info, Sparkles, AlertTriangle } from 'lucide-react';
import { useSettings } from '@/contexts/SettingsContext.jsx';

const PredictPage = () => {
  const { serverUrl } = useSettings();
  const [uploadView, setUploadView] = useState(true);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const { toast } = useToast();

  const handleImageSelect = (imageData) => {
    setUploadedImage(imageData);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!uploadedImage) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', uploadedImage.file);

      // Calling the FastAPI server
      const rawUrl = (serverUrl || 'http://127.0.0.1:8000').trim();
      const backendBase = rawUrl.replace(/0\.0\.0\.0/g, '127.0.0.1').replace(/\/+$/, '');
      const response = await fetch(`${backendBase}/analyze`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.status === 'error') {
        setError(data.message || data.detail || "An error occurred during analysis.");
        setLoading(false);
        return;
      }

      if (!response.ok) {
        throw new Error(data.detail || data.message || `Server error: ${response.status} ${response.statusText}`);
      }
      
      if (!data.primary_diagnosis) {
        throw new Error("Invalid response format from server. Missing primary_diagnosis.");
      }

      setAnalysisResult(data);
      setUploadView(false);

      toast({
        title: "Analysis complete",
        description: "Disease detection completed successfully.",
      });
    } catch (err) {
      console.error('Analysis error:', err);
      
      let errorMessage = err.message || 'Failed to analyze image. Please check your server connection.';
      if (err.name === 'TypeError' && (err.message === 'Failed to fetch' || err.message.includes('NetworkError') || err.message.includes('fetch'))) {
        const rawUrl = (serverUrl || 'http://127.0.0.1:8000').trim();
        const backendBase = rawUrl.replace(/0\.0\.0\.0/g, '127.0.0.1').replace(/\/+$/, '');
        errorMessage = `Network error: Could not connect to backend server at ${backendBase}. Ensure your FastAPI backend is running.`;
      }

      setError(errorMessage);
      
      toast({
        title: "Analysis failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setUploadedImage(null);
    setError(null);
  };

  const handleReset = () => {
    setUploadView(true);
    setUploadedImage(null);
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <>
      <Helmet>
        <title>Predict - Poultry Disease Detection System</title>
        <meta 
          name="description" 
          content="AI-powered poultry disease classification system using deep learning to detect healthy birds and common diseases." 
        />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-50 bg-size-200 animate-gradient-pulse py-16">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="mb-12 text-center">
            <h1 className="text-4xl md:text-6xl font-black text-gray-900 mb-6 drop-shadow-sm">Disease Detection Analysis</h1>
            <p className="text-gray-600 max-w-2xl mx-auto text-xl font-medium">Upload a clear image of the poultry to receive an instant AI-powered diagnostic assessment and actionable recommendations.</p>
          </div>

          <AnimatePresence mode="wait">
            {uploadView ? (
              <motion.div
                key="upload-view"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
                className="space-y-10"
              >
                {error && !loading && (
                  <ErrorAlert 
                    message={error} 
                    onDismiss={() => setError(null)} 
                  />
                )}

                <div className="bg-white rounded-[2.5rem] p-2 md:p-4 border border-gray-200 shadow-2xl">
                  <ImageUpload
                    onImageSelect={handleImageSelect}
                    onAnalyze={handleAnalyze}
                    onClear={handleClear}
                    selectedImage={uploadedImage}
                    isLoading={loading}
                  />
                </div>

                {loading && (
                  <div className="bg-white rounded-[2.5rem] p-12 border border-gray-200 shadow-xl flex justify-center">
                    <LoadingSpinner />
                  </div>
                )}

                {!uploadedImage && !loading && !error && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="bg-white rounded-[2.5rem] p-10 border border-gray-200 shadow-xl"
                  >
                    <div className="flex items-center gap-4 mb-8">
                      <div className="p-3 bg-gradient-to-br from-primary to-secondary rounded-2xl shadow-md">
                        <Info className="w-8 h-8 text-white" />
                      </div>
                      <h2 className="text-3xl font-black text-gray-900">How to Use</h2>
                    </div>
                    <ol className="space-y-6 text-gray-800">
                      <li className="flex items-start gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100 hover:border-primary/30 transition-colors">
                        <span className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary text-white shadow-md flex items-center justify-center font-black text-lg">1</span>
                        <span className="mt-1.5 font-bold text-lg">Upload a high-quality image of the poultry in JPG or PNG format. Ensure optimal lighting and visibility of the affected area for accurate analysis.</span>
                      </li>
                      <li className="flex items-start gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100 hover:border-primary/30 transition-colors">
                        <span className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary text-white shadow-md flex items-center justify-center font-black text-lg">2</span>
                        <span className="mt-1.5 font-bold text-lg">Initiate the AI-powered diagnostic analysis by clicking the "Analyze Image" button. The system will process your image using advanced deep learning models.</span>
                      </li>
                      <li className="flex items-start gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100 hover:border-primary/30 transition-colors">
                        <span className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary text-white shadow-md flex items-center justify-center font-black text-lg">3</span>
                        <span className="mt-1.5 font-bold text-lg">Review the comprehensive diagnostic report, including visual heatmaps, confidence scores, and actionable veterinary recommendations generated by the system.</span>
                      </li>
                      <li className="flex items-start gap-5 bg-red-50 p-5 rounded-2xl border border-red-100 hover:border-red-200 transition-colors">
                        <span className="flex-shrink-0 w-10 h-10 rounded-xl bg-red-500 text-white shadow-md flex items-center justify-center font-black text-lg">4</span>
                        <span className="mt-1.5 font-bold text-lg text-gray-900">
                          <span className="text-red-600 flex items-center gap-2 mb-1"><AlertTriangle className="w-5 h-5"/> Important:</span>
                          This system is specifically trained for poultry disease detection. Non-poultry images will not yield valid diagnostic results. Please ensure all uploaded images contain poultry subjects for accurate analysis.
                        </span>
                      </li>
                    </ol>
                  </motion.div>
                )}
              </motion.div>
            ) : (
              <motion.div
                key="results-view"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col gap-10"
              >
                <div className="flex justify-end">
                  <Button 
                    onClick={handleReset}
                    className="bg-gray-900 text-white hover:bg-primary hover:shadow-xl hover:scale-105 transition-all rounded-full px-8 py-6 text-lg font-bold border-none"
                  >
                    <RefreshCw className="w-5 h-5 mr-3" />
                    Analyze Another Image
                  </Button>
                </div>

                <div className="w-full">
                  <PredictionResult analysisResult={analysisResult} />
                </div>

                <div className="flex flex-col md:flex-row gap-8 items-stretch">
                  <div className="flex-1 h-[450px] overflow-hidden rounded-[2rem] border border-gray-200 shadow-xl">
                    <ProbabilityDistributionChart distribution={analysisResult?.distribution} />
                  </div>

                  <div className="flex-1 h-[450px] overflow-hidden rounded-[2rem] border border-gray-200 shadow-xl">
                    <ResultsVisualsSection 
                      originalImageBase64={analysisResult?.original_image_base64}
                      heatmapImageBase64={analysisResult?.heatmap_image_base64}
                    />
                  </div>
                </div>

                {analysisResult?.report && (
                  <div className="max-w-5xl mx-auto w-full mt-6">
                    <div className="bg-gradient-to-r from-primary via-indigo-600 to-purple-800 bg-size-200 animate-gradient-shift rounded-[2.5rem] p-8 md:p-12 shadow-2xl relative overflow-hidden text-white border border-white/20">
                      <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
                      <h3 className="text-3xl font-black mb-8 border-b border-white/20 pb-6 flex items-center gap-4 drop-shadow-md">
                        <div className="p-3 bg-white/20 rounded-2xl shadow-inner backdrop-blur-sm">
                          <Sparkles className="w-8 h-8 text-white" />
                        </div>
                        AI Diagnostic Report
                      </h3>
                      <div className="overflow-auto prose prose-lg prose-invert max-w-none font-medium drop-shadow-sm">
                        <MarkdownRenderer markdown={analysisResult.report} />
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </>
  );
};

export default PredictPage;
