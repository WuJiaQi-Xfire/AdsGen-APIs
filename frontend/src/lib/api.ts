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
  seeds: number[];
}

export interface PromptFile {
  id: string;
  name: string;
  content: string;
  selected: boolean;
}
export interface Style {
  id: string;
  name: string;
}
export interface StyleResponse {
  loraStyles: Style[];
  artStyles: Style[];
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

  //Get lora and art styles
  getStyles: async (): Promise<StyleResponse> => {
    try {
      const response = await fetch(`${API_BASE_URL}/get-styles/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`Failed to get styles: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to get styles");
    }
  },

  // Image Generation
  generateImage: async (
    selectedPrompts: PromptFile[],
    selectedStyles: string[],
    width: number,
    height: number,
    batchSize: number,
    keywords: string[],
    styleStrength: number
  ): Promise<ImageGenerationResponse> => {
    try {
      const formData = new FormData();
      formData.append("prompts", JSON.stringify(selectedPrompts));
      formData.append("styles", JSON.stringify(selectedStyles));
      formData.append("width", width.toString());
      formData.append("height", height.toString());
      formData.append("batch_size", batchSize.toString());
      formData.append("keywords", JSON.stringify(keywords));
      formData.append("style_strength", styleStrength.toString());

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
