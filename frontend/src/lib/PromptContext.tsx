import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { PromptFile, promptApi } from './api';
import { showToast } from './ShowToast';

interface PromptContextType {
  promptFiles: PromptFile[];
  isLoadingPrompts: boolean;
  loadPrompts: (forceReload?: boolean) => Promise<void>;
  togglePromptSelection: (id: number) => void;
  hasPrompt: boolean;
}

const PromptContext = createContext<PromptContextType | undefined>(undefined);

export const PromptProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [promptFiles, setPromptFiles] = useState<PromptFile[]>([]);
  const [isLoadingPrompts, setIsLoadingPrompts] = useState(false);
  const [hasPrompt, setHasPrompt] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  const loadPrompts = async (forceReload = false) => {
    // If prompts are already loaded and we're not forcing a reload, don't reload
    if (promptFiles.length > 0 && !isLoadingPrompts && !forceReload) {
      return;
    }

    setIsLoadingPrompts(true);
    try {
      const prompts = await promptApi.getPrompts();
      setPromptFiles(prompts);
      setHasPrompt(prompts.length > 0);
      setIsInitialized(true);
    } catch (error) {
      console.error("Error loading prompts:", error);
      showToast("Failed to load prompts");
    } finally {
      setIsLoadingPrompts(false);
    }
  };

  // Load prompts on initial mount
  useEffect(() => {
    if (!isInitialized) {
      loadPrompts();
    }
  }, [isInitialized]);

  const togglePromptSelection = (id: number) => {
    setPromptFiles((prev) =>
      prev.map((file) =>
        file.id === id ? { ...file, selected: !file.selected } : file
      )
    );
  };

  return (
    <PromptContext.Provider
      value={{
        promptFiles,
        isLoadingPrompts,
        loadPrompts,
        togglePromptSelection,
        hasPrompt,
      }}
    >
      {children}
    </PromptContext.Provider>
  );
};

export const usePrompts = (): PromptContextType => {
  const context = useContext(PromptContext);
  if (context === undefined) {
    throw new Error('usePrompts must be used within a PromptProvider');
  }
  return context;
};
