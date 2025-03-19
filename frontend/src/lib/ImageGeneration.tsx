import { useState, useRef } from "react";
import { showToast } from "@/lib/ShowToast";
import { getStyles } from "@/lib/ArtStyleList";

interface PromptFile {
  id: string;
  name: string;
  selected: boolean;
}

export const ImageGeneration = () => {
  const [promptFiles, setPromptFiles] = useState<PromptFile[]>([]);
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
    setIsGenerating(true);
    try {
      const selectedPrompts = promptFiles.filter((file) => file.selected);
      if (selectedPrompts.length === 0) {
        throw new Error("No prompts selected");
      }

      if (selectedStyles.length === 0) {
        throw new Error("No styles selected");
      }
      const formData = new FormData();
      formData.append("prompts", JSON.stringify(selectedPrompts));
      formData.append("styles", JSON.stringify(selectedStyles));
      formData.append("style_type", styleType);
      formData.append("style_strength", styleStrength.toString());
      formData.append("width", resolution.width.toString());
      formData.append("height", resolution.height.toString());
      formData.append("batch_size", batchSize.toString());
      formData.append("keywords", JSON.stringify(keywords));

      // Send request to backend
      const response = await fetch(
        "http://127.0.0.1:8000/api/generate-image/",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate image");
      }

      const data = await response.json();
      showToast("Your image has been generated successfully.");
      // Testing backend output
      console.log("Generated images:", data);
    } catch (error: any) {
      console.error("Error generating image:", error);
      showToast("There was an error generating your image. Please try again.");
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
    keywords,
    isGenerating,
    selectedStyles,
    styleType,
    searchQuery,
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
  };
};
