import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Button } from '@/components/ui/button.jsx';
import { useSettings } from '@/contexts/SettingsContext.jsx';
import { useToast } from '@/components/ui/use-toast.js';
import { CheckCircle2, XCircle, Loader2 } from 'lucide-react';

const SettingsModal = ({ open, onOpenChange }) => {
  const { serverUrl, setServerUrl, isConnected, isChecking, checkConnection } = useSettings();
  const [tempUrl, setTempUrl] = useState(serverUrl);
  const { toast } = useToast();

  useEffect(() => {
    if (open) {
      setTempUrl(serverUrl);
      checkConnection();
    }
  }, [open, serverUrl]);

  const handleSave = () => {
    setServerUrl(tempUrl);
    toast({
      title: "Settings saved",
      description: "Server URL has been updated successfully.",
    });
    onOpenChange(false);
  };

  const handleCancel = () => {
    setTempUrl(serverUrl);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Settings</DialogTitle>
          <DialogDescription>
            Configure your FastAPI server connection
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <label htmlFor="server-url" className="text-sm font-medium text-white">
              FastAPI Server URL
            </label>
            <Input
              id="server-url"
              type="text"
              value={tempUrl}
              onChange={(e) => setTempUrl(e.target.value)}
              placeholder="http://localhost:8000"
              className="text-white"
            />
          </div>

          <div className="flex items-center gap-2 p-3 rounded-lg bg-white/5 border border-purple-300/20">
            {isChecking ? (
              <>
                <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
                <span className="text-sm text-gray-300">Checking connection...</span>
              </>
            ) : isConnected ? (
              <>
                <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                <span className="text-sm text-emerald-400">Server connected</span>
              </>
            ) : (
              <>
                <XCircle className="w-5 h-5 text-red-500" />
                <span className="text-sm text-red-400">Server disconnected</span>
              </>
            )}
          </div>
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={handleCancel}
            className="bg-white/10 text-white border-purple-300/30 hover:bg-white/20"
          >
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            className="bg-gradient-to-r from-purple-500 to-blue-500 text-white hover:from-purple-600 hover:to-blue-600"
          >
            Save Changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default SettingsModal;