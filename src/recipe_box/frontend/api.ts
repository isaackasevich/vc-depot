// API service for Recipe Box backend
const API_BASE_URL = 'http://localhost:8000';

export interface Recipe {
  id: number;
  name: string;
  ingredients: string[];
  instructions: string[];
  prep_time: number;
  cook_time: number;
  servings: number;
  category: string;
  created_at?: string;
  updated_at?: string;
}

export interface RecipeCreate {
  name: string;
  ingredients: string[];
  instructions: string[];
  prep_time: number;
  cook_time: number;
  servings: number;
  category: string;
}

export interface RecipeUpdate {
  name?: string;
  ingredients?: string[];
  instructions?: string[];
  prep_time?: number;
  cook_time?: number;
  servings?: number;
  category?: string;
}

class RecipeAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Get all recipes
  async getRecipes(): Promise<Recipe[]> {
    return this.request<Recipe[]>('/recipes');
  }

  // Get a specific recipe by ID
  async getRecipe(id: number): Promise<Recipe> {
    return this.request<Recipe>(`/recipes/${id}`);
  }

  // Create a new recipe
  async createRecipe(recipe: RecipeCreate): Promise<Recipe> {
    return this.request<Recipe>('/recipes', {
      method: 'POST',
      body: JSON.stringify(recipe),
    });
  }

  // Update an existing recipe
  async updateRecipe(id: number, recipe: RecipeUpdate): Promise<Recipe> {
    return this.request<Recipe>(`/recipes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(recipe),
    });
  }

  // Delete a recipe
  async deleteRecipe(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/recipes/${id}`, {
      method: 'DELETE',
    });
  }

  // Get recipes by category
  async getRecipesByCategory(category: string): Promise<Recipe[]> {
    return this.request<Recipe[]>(`/recipes/category/${encodeURIComponent(category)}`);
  }

  // Get all categories
  async getCategories(): Promise<{ categories: string[] }> {
    return this.request<{ categories: string[] }>('/categories');
  }

  // Health check
  async healthCheck(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/');
  }
}

// Export a singleton instance
export const recipeAPI = new RecipeAPI();

// Export the class for testing or custom instances
export { RecipeAPI }; 