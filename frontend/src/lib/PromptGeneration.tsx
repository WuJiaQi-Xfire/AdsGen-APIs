import { useState } from "react";
import { showToast } from "@/lib/ShowToast";

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
    setIsGenerating(true);
    try {
      const formData = new FormData();
      formData.append("description", description);

      if (imageFile) {
        formData.append("reference_image", imageFile);
      } else if (imageUrl) {
        formData.append("reference_image_url", imageUrl);
      }

      const response = await fetch(
        "http://127.0.0.1:8000/api/generate-prompt/",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate prompt");
      }

      const data = await response.json();
      setGeneratedPrompt(data.generated_prompt || "");
      showToast("Your prompt has been generated successfully.");
    } catch (error) {
      console.error("Error generating prompt:", error);
      showToast("There was an error generating your prompt. Please try again.");
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
