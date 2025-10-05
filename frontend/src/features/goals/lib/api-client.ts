/**
 * HTTP API client for backend.goals
 * Consumes REST endpoints at /api/goals
 */

import type { Goal, GoalCreateInput, GoalUpdateInput, ApiError } from '../types';

const API_BASE_URL = process.env['NEXT_PUBLIC_API_URL'] || 'http://localhost:8000';

class GoalsApiClient {
  private async fetchJson<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        detail: response.statusText,
        status: response.status,
      }));
      throw new Error(error.detail || 'Request failed');
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  async listGoals(status?: 'active' | 'done'): Promise<{ goals: Goal[] }> {
    const params = status ? `?status=${status}` : '';
    return this.fetchJson(`/api/goals${params}`);
  }

  async getGoal(id: string): Promise<Goal> {
    return this.fetchJson(`/api/goals/${id}`);
  }

  async createGoal(input: GoalCreateInput): Promise<Goal> {
    return this.fetchJson('/api/goals', {
      method: 'POST',
      body: JSON.stringify(input),
    });
  }

  async updateGoal(id: string, input: GoalUpdateInput): Promise<Goal> {
    return this.fetchJson(`/api/goals/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(input),
    });
  }

  async deleteGoal(id: string): Promise<void> {
    return this.fetchJson(`/api/goals/${id}`, {
      method: 'DELETE',
    });
  }
}

export const goalsApi = new GoalsApiClient();
