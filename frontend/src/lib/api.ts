import { showToast } from "@/lib/ShowToast";
import axios from "axios";

// Base API URL - can be replaced with env variable in production
const API_BASE_URL = "http://127.0.0.1:8000/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

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

export interface GeneratedImageData {
  filename: string;
  data: string;
}

export interface ImageGenerationResponse {
  images: GeneratedImageData[];
}

export interface PromptFile {
  id: number;
  name: string;
  content: string;
  selected?: boolean;
  created_at?: string;
}
export interface Style {
  id: string;
  name: string;
  styleType: "lora" | "art";
}
export interface StyleResponse {
  loraStyles: Style[];
  artStyles: Style[];
}

export interface StyleSetting {
  id: string;
  styleStrength: number;
  batchSize: number;
  //aspectRatio: "1:1" | "16:9" | "9:16";
  styleType: "lora" | "art";
}

export interface ImageGenerationRequest {
  prompts: PromptFile[];
  style_settings: StyleSetting[];
  keywords: string[];
  stack_loras: boolean;
}

export class ApiService {
  // Prompt Generation
  static async generatePrompt(
    description: string,
    image?: File | null,
    image_url?: string | null
  ): Promise<PromptGenerationResponse> {
    try {
      const formData = new FormData();
      formData.append("description", description);

      if (image) {
        formData.append("image", image);
      } else if (image_url) {
        formData.append("image_url", image_url);
      }

      const response = await fetch(`${API_BASE_URL}/generate/prompt/`, {
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
  }

  // Keyword Extraction
  static async extractKeywords(
    image?: File | null,
    imageUrl?: string | null
  ): Promise<KeywordExtractionResponse> {
    try {
      const formData = new FormData();

      if (image) {
        formData.append("image", image);
      } else if (imageUrl) {
        formData.append("image_url", imageUrl);
      } else {
        throw new Error("No image provided");
      }

      const response = await fetch(`${API_BASE_URL}/generate/keywords/`, {
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
  }

  //Get lora and art styles
  static async getStyles(): Promise<StyleResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/styles/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`Failed to get styles: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to get styles");
    }
  }

  // Image Generation
  static async generateImage(
    selectedPrompts: PromptFile[],
    styleSettings: StyleSetting[],
    keywords: string[],
    stackLoras: boolean
  ): Promise<ImageGenerationResponse> {
    try {
      const formData = new FormData();
      formData.append("prompts", JSON.stringify(selectedPrompts));
      formData.append("style_settings", JSON.stringify(styleSettings));
      formData.append("keywords", JSON.stringify(keywords));
      formData.append("stack_loras", JSON.stringify(stackLoras));

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
  }

  // Get Generated Images
  static async getGeneratedImages(): Promise<{ images: GeneratedImageData[] }> {
    try {
      const response = await fetch(`${API_BASE_URL}/get-generated-images/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`Failed to get generated images: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to get generated images");
    }
  }
}

// Auth API services
export async function login(email: string, password: string) {
  // TODO: Replace with actual API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ token: "dummy-token", user: { email } });
    }, 1000);
  });
}

export async function signup(email: string, password: string) {
  // TODO: Replace with actual API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ token: "dummy-token", user: { email } });
    }, 1000);
  });
}

//Prompt database CRUD
export const promptApi = {
  getPrompts: async (skip = 0, limit = 100): Promise<PromptFile[]> => {
    try {
      const response = await apiClient.get("/prompts/", {
        params: { skip, limit },
      });
      return response.data.map((prompt) => ({
        ...prompt,
        name: prompt.prompt_name,
        selected: false,
      }));
    } catch (error) {
      console.error("Failed to fetch prompts", error);
      return [];
    }
  },

  getPrompt: async (id: number): Promise<PromptFile | null> => {
    try {
      const response = await apiClient.get(`/prompts/${id}`);
      return {
        ...response.data,
        name: response.data.prompt_name,
        selected: false,
      };
    } catch (error) {
      console.error(`Failed to fetch prompt with ID ${id}`, error);
      return null;
    }
  },

  createPrompt: async (data: {
    name: string;
    content: string;
  }): Promise<{
    id: number;
    message: string;
    success: boolean;
  }> => {
    try {
      const response = await apiClient.post<{ id: number; message: string }>(
        "/prompts/",
        {
          prompt_name: data.name,
          content: data.content,
        }
      );
      return {
        ...response.data,
        success: true,
      };
    } catch (error) {
      console.error("Failed to create prompt", error);
      return {
        id: -1,
        message: "Failed to create prompt",
        success: false,
      };
    }
  },

  deletePrompt: async (
    id: number
  ): Promise<{
    success: boolean;
    message: string;
  }> => {
    try {
      const response = await apiClient.delete<{ message: string }>(
        `/prompts/${id}`
      );
      return {
        success: true,
        message: response.data.message,
      };
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        return {
          success: true,
          message: "Prompt already deleted",
        };
      }
      console.error(`Failed to delete prompt with ID ${id}`, error);
      return {
        success: false,
        message: `Failed to delete prompt with ID ${id}`,
      };
    }
  },
};
