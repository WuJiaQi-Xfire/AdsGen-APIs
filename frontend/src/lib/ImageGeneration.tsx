import { useState, useEffect, useRef } from "react";
import { showToast } from "@/lib/ShowToast";
import { v4 as uuidv4 } from "uuid";
import { ApiService, PromptFile } from "@/lib/api";

export interface Style {
  id: string;
  name: string;
  styleType: "lora" | "art";
}

export interface StyleResponse {
  loraStyles: Style[];
  artStyles: Style[];
}
export interface GeneratedImage {
  url: string;
  seed: number;
}

export const ImageGeneration = () => {
  const [promptFiles, setPromptFiles] = useState<PromptFile[]>([]);
  const [hasPrompt, setHasPrompt] = useState(false);
  const [promptFileName, setPromptFileName] = useState("");
  const [selectedStyles, setSelectedStyles] = useState<string[]>([]);
  const [styleType, setStyleType] = useState<"lora" | "art">("lora");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectMode, setSelectMode] = useState<"multiple">("multiple");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const promptFileInputRef = useRef<HTMLInputElement>(null);
  const [loraStyles, setLoraStyles] = useState<Style[]>([]);
  const [artStyles, setArtStyles] = useState<Style[]>([]);
  const [isLoadingPrompts, setIsLoadingPrompts] = useState(false);

  useEffect(() => {
    const fetchStyles = async () => {
      try {
        const styles = await ApiService.getStyles();
        setLoraStyles(styles.loraStyles);
        setArtStyles(styles.artStyles);
      } catch (error) {
        console.error("Error fetching styles:", error);
      }
    };
    fetchStyles();
    loadPrompts();
  }, []);
  
  const loadPrompts = async () => {
    setIsLoadingPrompts(true);
    try {
      const prompts = await ApiService.getPrompts();
      setPromptFiles(prompts);
      setHasPrompt(prompts.length > 0);
    } catch (error) {
      console.error("Error loading prompts:", error);
      showToast("Failed to load prompts from the database");
    } finally {
      setIsLoadingPrompts(false);
    }
  };

  const currentStyles = styleType === "lora" ? loraStyles : artStyles;

  const filteredStyles = searchQuery
    ? currentStyles.filter((style) =>
        style.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : currentStyles;

  const handlePromptFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const filesArray = Array.from(e.target.files);
    let filesProcessed = 0;
    const totalFiles = filesArray.length;
    
    for (const file of filesArray) {
      try {
        const content = await readFileAsText(file);
        const promptName = file.name.replace(/\.txt$/, '');
        
        // Save to database
        await ApiService.savePrompt(promptName, content);
        filesProcessed++;
        
        if (filesProcessed === totalFiles) {
          showToast("Upload successful. Prompts saved to database.");
          // Reload prompts from database
          await loadPrompts();
        }
      } catch (error) {
        console.error(`Error processing file ${file.name}:`, error);
        showToast(`There was an error processing the file ${file.name}.`);
        filesProcessed++;
      }
    }
  };
  
  const readFileAsText = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          resolve(event.target.result as string);
        } else {
          reject(new Error('Failed to read file'));
        }
      };
      reader.onerror = () => reject(new Error(`Error reading file ${file.name}`));
      reader.readAsText(file);
    });
  };

  const handlePromptUpload = () => {
    if (promptFileInputRef.current) {
      promptFileInputRef.current.click();
    }
  };

  const togglePromptSelection = (id: string) => {
    setPromptFiles((prev) =>
      prev.map((file) =>
        file.id === id ? { ...file, selected: !file.selected } : file
      )
    );
  };

  const toggleStyleSelection = (styleId: string) => {
    if (selectedStyles.includes(styleId)) {
      setSelectedStyles(selectedStyles.filter((id) => id !== styleId));
    } else {
      setSelectedStyles([...selectedStyles, styleId]);
    }
  };

  const selectAllStyles = () => {
    // Get all currently filtered styles
    const filteredStyleIds = filteredStyles.map((style) => style.id);
    
    // Keep existing selections that aren't in the current filtered list
    const existingSelections = selectedStyles.filter(
      (id) => !currentStyles.some((style) => style.id === id)
    );
    
    // Combine with all filtered styles
    setSelectedStyles([...existingSelections, ...filteredStyleIds]);
  };

  const clearStyleSelection = () => {
    setSelectedStyles([]);
  };

  const selectRandomStyle = () => {
    const randomIndex = Math.floor(Math.random() * filteredStyles.length);
    setSelectedStyles([filteredStyles[randomIndex].id]);
  };

  return {
    promptFiles,
    hasPrompt,
    promptFileName,
    selectedStyles,
    styleType,
    setStyleType,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    fileInputRef,
    promptFileInputRef,
    handlePromptUpload,
    handlePromptFileUpload,
    toggleStyleSelection,
    selectAllStyles,
    clearStyleSelection,
    selectRandomStyle,
    filteredStyles,
    togglePromptSelection,
    loraStyles,
    artStyles,
    loadPrompts,
    isLoadingPrompts,
  };
};
