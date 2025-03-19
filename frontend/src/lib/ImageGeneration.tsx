import { useState, useRef } from "react";
import { showToast } from "@/lib/ShowToast";
import { getStyles } from "@/lib/ArtStyleList";

interface PromptFile {
  id: string;
  name: string;
  selected: boolean;
}

export const ImageGeneration = () => {
  const [prompt, setPrompt] = useState("");
  const [hasPrompt, setHasPrompt] = useState(false);
  const [promptFiles, setPromptFiles] = useState<PromptFile[]>([]);
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
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
  const [promptFileName, setPromptFileName] = useState("");
  const [hasReferenceImage, setHasReferenceImage] = useState(false);
  const [referenceImageFileName, setReferenceImageFileName] = useState("");
  const [referenceImageUrl, setReferenceImageUrl] = useState("");
  const { filteredStyles } = getStyles(styleType, searchQuery);

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

  const handleReferenceImageUpload = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (e.target.files && e.target.files.length === 1) {
      const file = e.target.files[0];
      setReferenceImageFileName(file.name);
      setHasReferenceImage(true);
      setReferenceImageUrl("");

      showToast("${file.name} has been selected as reference.");
    }
  };

  const clearReferenceImage = () => {
    setHasReferenceImage(false);
    setReferenceImageFileName("");
    setReferenceImageUrl("");
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate generation
    setTimeout(() => {
      setIsGenerating(false);
      showToast("Your image has been generated successfully.");
    }, 1500);
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
    prompt,
    setPrompt,
    hasPrompt,
    setHasPrompt,
    promptFiles,
    promptFileName,
    keyword,
    setKeyword,
    keywords,
    setKeywords,
    isGenerating,
    selectedStyles,
    styleType,
    setStyleType,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    styleStrength,
    setStyleStrength,
    resolution,
    setResolution,
    batchSize,
    setBatchSize,
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
    hasReferenceImage,
    referenceImageFileName,
    referenceImageUrl,
    setReferenceImageUrl,
    handleGenerate,
    handleReferenceImageUpload,
    clearReferenceImage,
  };
};
