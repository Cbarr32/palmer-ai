/**
 * Palmer AI API Client
 * Connects to FastAPI backend with proper error handling
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class PalmerAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async chat(message: string, context?: any) {
    const response = await fetch(`${this.baseURL}/palmer/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        context,
        distributor_id: 'frontend-user',
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('distributor_id', 'frontend-user');

    const response = await fetch(`${this.baseURL}/palmer/upload-and-chat`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload Error: ${response.status}`);
    }

    return response.json();
  }

  async healthCheck() {
    const response = await fetch(`${this.baseURL}/health`);
    return response.json();
  }
}

export const palmerAPI = new PalmerAPI();
