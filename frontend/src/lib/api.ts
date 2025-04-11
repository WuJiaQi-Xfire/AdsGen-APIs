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

export interface GeneratedImageData {
  filename: string;
  data: string;
}

export interface ImageGenerationResponse {
  images: GeneratedImageData[];
}

export interface PromptFile {
  id: string;
  name: string;
  content: string;
  selected: boolean;
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
  // Database Prompt Management
  static async savePrompt(
    promptName: string,
    content: string
  ): Promise<{ id: number }> {
    try {
      const response = await fetch(`${API_BASE_URL}/prompts/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt_name: promptName,
          content: content,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to save prompt: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to save prompt");
    }
  }

  static async getPrompts(): Promise<PromptFile[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/prompts/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`Failed to get prompts: ${response.status}`);
      }

      const prompts = await response.json();
      return prompts.map((prompt: any) => ({
        id: prompt.id.toString(),
        name: prompt.prompt_name,
        content: prompt.content,
        selected: false,
        created_at: prompt.created_at,
      }));
    } catch (error) {
      return handleApiError(error, "Failed to get prompts");
    }
  }

  static async getPrompt(id: string): Promise<PromptFile> {
    try {
      const response = await fetch(`${API_BASE_URL}/prompts/${id}`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`Failed to get prompt: ${response.status}`);
      }

      const prompt = await response.json();
      return {
        id: prompt.id.toString(),
        name: prompt.prompt_name,
        content: prompt.content,
        selected: false,
        created_at: prompt.created_at,
      };
    } catch (error) {
      return handleApiError(error, "Failed to get prompt");
    }
  }

  static async deletePrompt(id: string): Promise<{ message: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/prompts/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Failed to delete prompt: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return handleApiError(error, "Failed to delete prompt");
    }
  }

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
  }

  //Get lora and art styles
  static async getStyles(): Promise<StyleResponse> {
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
      resolve({ token: 'dummy-token', user: { email } });
    }, 1000);
  });
}

export async function signup(email: string, password: string) {
  // TODO: Replace with actual API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ token: 'dummy-token', user: { email } });
    }, 1000);
  });
}
