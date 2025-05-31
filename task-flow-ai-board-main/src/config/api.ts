// API Configuration
export const API_CONFIG = {
  BASE_URL: 'https://internship-task-roles-allocatement.onrender.com',
  ENDPOINTS: {
    GENERATE_TASKS: '/generate-tasks',
  },
  TIMEOUT: 30000, // 30 seconds timeout for API calls
} as const;

// API request interface
export interface ProjectRequest {
  project_description: string;
}

export interface TaskResponse {
  selected_roles: string[];
  role_tasks: Record<string, string[]>;
}

// API utility function to generate tasks
export const generateTasks = async (projectDescription: string): Promise<TaskResponse> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);

  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.GENERATE_TASKS}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        project_description: projectDescription
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout. Please try again.');
    }
    throw error;
  }
}; 