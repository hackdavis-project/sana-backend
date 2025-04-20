import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Base API types
interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// User types
interface User {
  id: string;
  username: string;
}

interface AuthResponse {
  user: User;
  token: string;
}

interface LoginRequest {
  username: string;
  password: string;
}

interface RegisterRequest {
  username: string;
  password: string;
}

// Journal types
interface JournalEntry {
  id: string;
  content: string;
  createdAt: string;
  isShared: boolean;
  category?: string;
  feelingRating: number;
}

interface CreateJournalEntryRequest {
  content: string;
  feelingRating: number;
  isShared?: boolean;
}

interface UpdateJournalEntryRequest {
  id: string;
  content?: string;
  isShared?: boolean;
}

// Resource types
interface Resource {
  id: string;
  name: string;
  description: string;
  phone?: string;
  website?: string;
  category: string;
}

// Community types
interface SharedEntry {
  id: string;
  content: string;
  category: string;
  createdAt: string;
}

// Feelings tracker types
interface FeelingData {
  entries: {
    date: string;
    rating: number;
  }[];
}

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL = 'http://localhost:8000/api') {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
  }

  // Auth methods
  async login(request: LoginRequest): Promise<ApiResponse<AuthResponse>> {
    const response = await this.client.post<ApiResponse<AuthResponse>>('/auth/login', request);
    if (response.data.success && response.data.data.token) {
      this.token = response.data.data.token;
    }
    return response.data;
  }

  async register(request: RegisterRequest): Promise<ApiResponse<AuthResponse>> {
    const response = await this.client.post<ApiResponse<AuthResponse>>('/auth/register', request);
    return response.data;
  }

  async logout(): Promise<ApiResponse<null>> {
    this.token = null;
    return { success: true, data: null };
  }

  // Journal methods
  async getJournalEntries(): Promise<ApiResponse<JournalEntry[]>> {
    const response = await this.client.get<ApiResponse<JournalEntry[]>>('/journal');
    return response.data;
  }

  async getJournalEntry(id: string): Promise<ApiResponse<JournalEntry>> {
    const response = await this.client.get<ApiResponse<JournalEntry>>(`/journal/${id}`);
    return response.data;
  }

  async createJournalEntry(request: CreateJournalEntryRequest): Promise<ApiResponse<JournalEntry>> {
    const response = await this.client.post<ApiResponse<JournalEntry>>('/journal', request);
    return response.data;
  }

  async updateJournalEntry(request: UpdateJournalEntryRequest): Promise<ApiResponse<JournalEntry>> {
    const response = await this.client.put<ApiResponse<JournalEntry>>(`/journal/${request.id}`, request);
    return response.data;
  }

  async deleteJournalEntry(id: string): Promise<ApiResponse<null>> {
    const response = await this.client.delete<ApiResponse<null>>(`/journal/${id}`);
    return response.data;
  }

  async toggleJournalEntrySharing(id: string, isShared: boolean): Promise<ApiResponse<JournalEntry>> {
    const response = await this.client.patch<ApiResponse<JournalEntry>>(`/journal/${id}/share`, { isShared });
    return response.data;
  }

  // Community methods
  async getSharedEntries(category?: string): Promise<ApiResponse<SharedEntry[]>> {
    const url = category ? `/community?category=${category}` : '/community';
    const response = await this.client.get<ApiResponse<SharedEntry[]>>(url);
    return response.data;
  }

  // Resources methods
  async getResources(): Promise<ApiResponse<Resource[]>> {
    const response = await this.client.get<ApiResponse<Resource[]>>('/resources');
    return response.data;
  }

  async getResourcesByCategory(category: string): Promise<ApiResponse<Resource[]>> {
    const response = await this.client.get<ApiResponse<Resource[]>>(`/resources?category=${category}`);
    return response.data;
  }

  async getResourceSuggestions(journalEntryId: string): Promise<ApiResponse<Resource[]>> {
    const response = await this.client.get<ApiResponse<Resource[]>>(`/resources/suggest/${journalEntryId}`);
    return response.data;
  }

  // Feelings tracker methods
  async getFeelingData(): Promise<ApiResponse<FeelingData>> {
    const response = await this.client.get<ApiResponse<FeelingData>>('/feelings');
    return response.data;
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();

// Export types
export type {
  ApiResponse,
  User,
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  JournalEntry,
  CreateJournalEntryRequest,
  UpdateJournalEntryRequest,
  Resource,
  SharedEntry,
  FeelingData
}; 