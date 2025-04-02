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
            id: uuidv4(),
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

  const toggleStyleSelection = (styleId: string) => {
    if (selectedStyles.includes(styleId)) {
      setSelectedStyles(selectedStyles.filter((id) => id !== styleId));
    } else {
      setSelectedStyles([...selectedStyles, styleId]);
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
  };
};
