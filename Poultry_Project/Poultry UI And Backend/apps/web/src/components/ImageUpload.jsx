import React, { useCallback, useState } from 'react';
import { UploadCloud, X, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';

const ImageUpload = ({ onImageSelect, onAnalyze, onClear, selectedImage, isLoading }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      processFile(file);
    }
  }, []);

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      onImageSelect({
        file,
        preview: reader.result
      });
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="w-full flex flex-col items-center">
      {!selectedImage ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`w-full relative overflow-hidden rounded-2xl border-3 border-dashed transition-all duration-300 flex flex-col items-center justify-center p-12 cursor-pointer group bg-size-200 animate-gradient-shift
            ${isDragging 
              ? 'border-white bg-gradient-to-br from-primary via-secondary to-blue-600 scale-[1.02] shadow-2xl shadow-primary/40' 
              : 'border-primary/50 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 hover:border-primary hover:from-indigo-900 hover:via-purple-900 hover:to-indigo-900 hover:shadow-xl'
            }`}
        >
          <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <div className="w-20 h-20 mb-6 rounded-full bg-white/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300 group-hover:bg-white/20 shadow-inner backdrop-blur-sm">
            <UploadCloud className="w-10 h-10 text-white drop-shadow-md" />
          </div>
          
          <h3 className="text-2xl font-black text-white mb-2 drop-shadow-md">Upload Poultry Image</h3>
          <p className="text-gray-200 text-center max-w-md mb-6 font-medium drop-shadow-sm">
            Drag and drop your image here, or click to browse your files. Ensure the image is clear and well-lit.
          </p>
          
          <label className="relative z-10">
            <span className="bg-white text-primary hover:bg-gray-100 px-8 py-3 rounded-full font-black shadow-lg hover:shadow-xl transition-all cursor-pointer inline-block hover:scale-105">
              Browse Files
            </span>
            <input
              type="file"
              className="hidden"
              accept="image/*"
              onChange={handleFileInput}
            />
          </label>
        </div>
      ) : (
        <div className="w-full flex flex-col items-center animate-in fade-in zoom-in duration-300 p-6 rounded-3xl bg-gradient-to-br from-gray-50 via-white to-gray-100 bg-size-200 animate-gradient-pulse shadow-inner border border-gray-200">
          <div className="relative w-full max-w-md rounded-2xl overflow-hidden shadow-2xl border-4 border-white group">
            <img 
              src={selectedImage.preview} 
              alt="Selected poultry" 
              className="w-full h-auto object-cover max-h-[400px]"
            />
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
              <Button 
                variant="destructive" 
                size="icon"
                onClick={onClear}
                className="rounded-full w-14 h-14 shadow-2xl hover:scale-110 transition-transform bg-red-500 hover:bg-red-600 border-2 border-white"
              >
                <X className="w-8 h-8 text-white" />
              </Button>
            </div>
          </div>
          
          <div className="mt-8 flex gap-4 w-full max-w-md">
            <Button 
              variant="outline" 
              onClick={onClear}
              disabled={isLoading}
              className="flex-1 border-gray-300 hover:bg-gray-100 text-gray-800 font-bold py-6 rounded-xl"
            >
              Cancel
            </Button>
            <Button 
              onClick={onAnalyze}
              disabled={isLoading}
              className="flex-1 bg-gradient-to-r from-primary to-secondary bg-size-200 animate-gradient-shift text-white shadow-lg hover:shadow-primary/40 hover:scale-105 transition-all font-black py-6 rounded-xl border-none"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <div className="w-5 h-5 border-3 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing...
                </span>
              ) : (
                <span className="flex items-center gap-2 text-lg">
                  <Sparkles className="w-5 h-5" />
                  Analyze Image
                </span>
              )}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;