import { showToast } from "@/lib/ShowToast";

// Base API URL - can be replaced with env variable in production
const API_BASE_URL = "http://127.0.0.1:8000/api";

const handleApiError = (error: any, customMessage?: string) => {
  console.error("API Error:", error);
  showToast(customMessage || "An unexpected error occurred. Please try again.");
  throw error;
};

export interface PromptGenerationResponse {
  generated_prompt: string;
}

export interface KeywordExtractionResponse {
  keywords: string[];
}

export interface ImageGenerationResponse {
  images: string[];
  job_id?: string;
}

export interface PromptFile {
  id: string;
  name: string;
  content: string;
  selected: boolean;
}

export const ApiService = {
  // Prompt Generation
  generatePrompt: async (
    description: string,
    image?: File | null,
    image_url?: string | null
  ): Promise<PromptGenerationResponse> => {
    try {
      const formData = new FormData();
      formData.append("description", description);

      if (image) {
        formData.append("image", image);
      } else if (image_url) {
        formData.append("image_url", image_url);
      }

      const response = await fetch(`${API_BASE_URL}/generate-prompt/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Failed to generate prompt: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to generate prompt");
    }
  },

  // Keyword Extraction
  extractKeywords: async (
    image?: File | null,
    imageUrl?: string | null
  ): Promise<KeywordExtractionResponse> => {
    try {
      const formData = new FormData();

      if (image) {
        formData.append("image", image);
      } else if (imageUrl) {
        formData.append("image_url", imageUrl);
      } else {
        throw new Error("No image provided");
      }

      const response = await fetch(`${API_BASE_URL}/extract-keywords/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Failed to extract keywords: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to extract keywords");
    }
  },

  // Image Generation
  generateImage: async (
    selectedPrompts: PromptFile[],
    selectedStyles: string[],
    styleType: "lora" | "art",
    styleStrength: number,
    width: number,
    height: number,
    batchSize: number,
    keywords: string[]
  ): Promise<ImageGenerationResponse> => {
    try {
      const formData = new FormData();
      formData.append("prompts", JSON.stringify(selectedPrompts));
      formData.append("styles", JSON.stringify(selectedStyles));
      formData.append("style_type", styleType);
      formData.append("style_strength", styleStrength.toString());
      formData.append("width", width.toString());
      formData.append("height", height.toString());
      formData.append("batch_size", batchSize.toString());
      formData.append("keywords", JSON.stringify(keywords));

      const response = await fetch(`${API_BASE_URL}/generate-image/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Failed to generate image: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to generate image");
    }
  },
};
