import { useState } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService } from "@/lib/api";

export const PromptGeneration = () => {
  const [description, setDescription] = useState(
    "Example: 50/50 split image, depicting the evil and good side of a place"
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPrompt, setGeneratedPrompt] = useState("");
  const [hasReferenceImage, setHasReferenceImage] = useState(false);
  const [fileName, setFileName] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);

  const handleGenerate = async () => {
    if (!description.trim()) {
      showToast("Please enter a description for your ad template.");
      return;
    }
    setIsGenerating(true);
    try {
      const response = await ApiService.generatePrompt(
        description,
        imageFile,
        imageUrl
      );
      setGeneratedPrompt(response.generated_prompt);
      showToast("Your ad template prompt has been generated successfully.");
    } catch (error) {
      console.error("Error in handleGenerate:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReferenceImageUpload = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (e.target.files && e.target.files.length === 1) {
      const file = e.target.files[0];
      setHasReferenceImage(true);
      setFileName(file.name);
      setImageUrl("");
      showToast("Your reference image will be used in the prompt generation.");
    }
  };

  const clearReferenceImage = () => {
    setHasReferenceImage(false);
    setFileName("");
    setImageUrl("");
    setImageFile(null);
  };

  return {
    description,
    setDescription,
    isGenerating,
    generatedPrompt,
    hasReferenceImage,
    fileName,
    imageUrl,
    setImageUrl,
    handleGenerate,
    handleReferenceImageUpload,
    clearReferenceImage,
  };
};
