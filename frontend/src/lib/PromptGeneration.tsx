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

  const handleGenerate = () => {
    setIsGenerating(true);

    // Text as placeholder for now, TODO Call GPT to generate prompt
    //Loading time fix for now, TODO load prompt after receiving response
    setTimeout(() => {
      setIsGenerating(false);
      setGeneratedPrompt(
        "You are an AI artist specializing in dynamic split-screen advertisements. " +
          "Generate a detailed image description using:  " +
          "- **Art Style**: [Use verbatim from {art_style_list}]" +
          "- **Theme**: {Keywords}  - **Structure**: Central region (75%), vertical sidebar (25%)." +
          "- **Intent**: Contrast 'problem state' (central) with 'solution state' (sidebar)."
      );

      showToast("Your ad template prompt has been generated successfully.");
    }, 1500);
  };

  const handleReferenceImageUpload = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    // TODO: File handling for image upload
    if (e.target.files && e.target.files.length === 1) {
      setHasReferenceImage(true);
      setFileName(e.target.files[0].name);
      setImageUrl("");
      showToast("Your reference image will be used in the prompt generation.");
    }
  };

  const clearReferenceImage = () => {
    setHasReferenceImage(false);
    setFileName("");
    setImageUrl("");
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
