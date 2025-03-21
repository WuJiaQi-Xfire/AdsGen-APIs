import { useState, useEffect, useRef } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService, PromptFile } from "@/lib/api";

export interface Style {
  id: string;
  name: string;
}

export interface StyleResponse {
  loraStyles: Style[];
  artStyles: Style[];
}
export const ImageGeneration = () => {
  const [promptFiles, setPromptFiles] = useState<PromptFile[]>([]);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [hasPrompt, setHasPrompt] = useState(false);
  const [promptFileName, setPromptFileName] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedStyles, setSelectedStyles] = useState<string[]>([]);
  const [styleType, setStyleType] = useState<"lora" | "art">("lora");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectMode, setSelectMode] = useState<"single" | "multiple">("single");
  const [styleStrength, setStyleStrength] = useState(80);
  const [resolution, setResolution] = useState({ width: 1024, height: 1024 });
  const [batchSize, setBatchSize] = useState(1);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const promptFileInputRef = useRef<HTMLInputElement>(null);
  const [loraStyles, setLoraStyles] = useState<Style[]>([]);
  const [artStyles, setArtStyles] = useState<Style[]>([]);

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
  }, []);

  const currentStyles = styleType === "lora" ? loraStyles : artStyles;

  const filteredStyles = searchQuery
    ? currentStyles.filter((style) =>
        style.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : currentStyles;

  const handlePromptFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const filesArray = Array.from(e.target.files);
    const newPromptFiles: PromptFile[] = [];
    let filesProcessed = 0;
    filesArray.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          const newFile: PromptFile = {
            id: crypto.randomUUID(),
            name: file.name,
            content: event.target.result as string,
            selected: false,
          };

          newPromptFiles.push(newFile);
          filesProcessed++;
          if (filesProcessed === filesArray.length) {
            setPromptFiles((prev) => [...prev, ...newPromptFiles]);
            setHasPrompt(true);
            showToast(
              "Upload successful. Please select the prompts you want to use."
            );
          }
        }
      };

      reader.onerror = () => {
        showToast("There was an error reading the file ${file.name}.");
        filesProcessed++;
      };

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

  const handleGenerate = async () => {
    if (promptFiles.length === 0) {
      showToast("Please upload at least one prompt.");
      return;
    }
    const selectedPrompts = promptFiles.filter((file) => file.selected);

    if (selectedPrompts.length === 0) {
      showToast("Please select at least one prompt.");
      return;
    }

    if (selectedStyles.length === 0) {
      showToast("Please select at least one style.");
      return;
    }
    setIsGenerating(true);
    try {
      const response = await ApiService.generateImage(
        selectedPrompts,
        selectedStyles,
        styleType,
        styleStrength,
        resolution.width,
        resolution.height,
        batchSize,
        keywords
      );
      showToast("Your image has been generated successfully.");
      // Testing backend output
      console.log("Generated images:", response);
    } catch (error: any) {
      console.error("Error handleGenerate:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const toggleStyleSelection = (styleId: string) => {
    if (selectMode === "single") {
      setSelectedStyles([styleId]);
    } else {
      if (selectedStyles.includes(styleId)) {
        setSelectedStyles(selectedStyles.filter((id) => id !== styleId));
      } else {
        setSelectedStyles([...selectedStyles, styleId]);
      }
    }
  };

  const selectAllStyles = () => {
    setSelectedStyles(filteredStyles.map((style) => style.id));
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
    keywords,
    isGenerating,
    selectedStyles,
    styleType,
    setStyleType,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    styleStrength,
    resolution,
    batchSize,
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
    handleGenerate,
    loraStyles,
    artStyles,
  };
};
