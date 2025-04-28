import { useState } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService } from "@/lib/api";

export const PromptGeneration = () => {
  const [description, setDescription] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPrompt, setGeneratedPrompt] = useState("");
  const [hasReferenceImage, setHasReferenceImage] = useState(false);
  const [fileName, setFileName] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [triggerHealthCheck, setTriggerHealthCheck] = useState(false);

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
      //console.log(response);
      setGeneratedPrompt(response.generated_prompt);
      showToast("Your ad template prompt has been generated successfully.");
    } catch (error) {
      console.error("Error in handleGenerate:", error);
      // Trigger health check when generation fails
      setTriggerHealthCheck(prev => !prev);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReferenceImageUpload = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (e.target.files && e.target.files.length === 1) {
      const file = e.target.files[0];
      setImageFile(file);
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
    triggerHealthCheck,
  };
};
