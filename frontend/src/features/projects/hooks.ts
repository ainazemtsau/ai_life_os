import { useState, useEffect, useCallback } from "react";

import type { Project, Task } from "@/features/projects/types";

// Mock API service - this would connect to your actual backend API
const projectsApi = {
  getProjects: async (goalId?: string): Promise<Project[]> => {
    // This would be an actual API call in a real implementation
    // For now, returning mock data
    console.log("Fetching projects", goalId);
    return Promise.resolve([]);
  },

  createProject: async (
    project: Omit<Project, "id" | "created_at" | "updated_at">,
  ): Promise<Project> => {
    // This would be an actual API call in a real implementation
    console.log("Creating project", project);
    return Promise.resolve({
      ...project,
      id: "new-id", // This would come from the API response
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  },

  updateProject: async (project: Project): Promise<Project> => {
    // This would be an actual API call in a real implementation
    console.log("Updating project", project);
    return Promise.resolve(project);
  },

  deleteProject: async (id: string): Promise<void> => {
    // This would be an actual API call in a real implementation
    console.log("Deleting project", id);
    return Promise.resolve();
  },

  getTasks: async (projectId?: string): Promise<Task[]> => {
    // This would be an actual API call in a real implementation
    // For now, returning mock data
    console.log("Fetching tasks", projectId);
    return Promise.resolve([]);
  },

  createTask: async (task: Omit<Task, "id" | "created_at" | "updated_at">): Promise<Task> => {
    // This would be an actual API call in a real implementation
    console.log("Creating task", task);
    return Promise.resolve({
      ...task,
      id: "new-id", // This would come from the API response
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  },

  updateTask: async (task: Task): Promise<Task> => {
    // This would be an actual API call in a real implementation
    console.log("Updating task", task);
    return Promise.resolve(task);
  },

  deleteTask: async (id: string): Promise<void> => {
    // This would be an actual API call in a real implementation
    console.log("Deleting task", id);
    return Promise.resolve();
  },
};

// Return type for hooks
interface UseProjectsReturn {
  projects: Project[];
  loading: boolean;
  error?: string;
  refetch: () => void;
}

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error?: string;
  refetch: () => void;
}

interface UseProjectMutationReturn {
  mutate: (project: Project) => Promise<void>;
  loading: boolean;
  error?: string;
}

interface UseTaskMutationReturn {
  mutate: (task: Task) => Promise<void>;
  loading: boolean;
  error?: string;
}

export function useProjects(goalId?: string): UseProjectsReturn {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | undefined>(undefined);

  const fetchProjects = useCallback(async () => {
    try {
      setLoading(true);
      setError(undefined);
      const data = await projectsApi.getProjects(goalId);
      setProjects(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch projects");
    } finally {
      setLoading(false);
    }
  }, [goalId]);

  useEffect(() => {
    fetchProjects().catch((err) => {
      console.error("Error fetching projects:", err);
    });
  }, [fetchProjects]);

  const refetch = useCallback(() => {
    fetchProjects().catch((err) => {
      console.error("Error fetching projects:", err);
    });
  }, [fetchProjects]);

  return error ? { projects, loading, error, refetch } : { projects, loading, refetch };
}

export function useTasks(projectId?: string): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | undefined>(undefined);

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(undefined);
      const data = await projectsApi.getTasks(projectId);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    fetchTasks().catch((err) => {
      console.error("Error fetching tasks:", err);
    });
  }, [fetchTasks]);

  const refetch = useCallback(() => {
    fetchTasks().catch((err) => {
      console.error("Error fetching tasks:", err);
    });
  }, [fetchTasks]);

  return error ? { tasks, loading, error, refetch } : { tasks, loading, refetch };
}

export function useCreateProject(): UseProjectMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (project: Project) => {
    try {
      setLoading(true);
      setError(undefined);
      const newProject = await projectsApi.createProject(project);
      // In a real implementation, you might update the cache here
      console.log("Created project:", newProject);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useUpdateProject(): UseProjectMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (project: Project) => {
    try {
      setLoading(true);
      setError(undefined);
      const updatedProject = await projectsApi.updateProject(project);
      // In a real implementation, you might update the cache here
      console.log("Updated project:", updatedProject);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update project");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useDeleteProject(): UseProjectMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (project: Project) => {
    try {
      setLoading(true);
      setError(undefined);
      await projectsApi.deleteProject(project.id);
      // In a real implementation, you might update the cache here
      console.log("Deleted project:", project.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete project");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useCreateTask(): UseTaskMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (task: Task) => {
    try {
      setLoading(true);
      setError(undefined);
      const newTask = await projectsApi.createTask(task);
      // In a real implementation, you might update the cache here
      console.log("Created task:", newTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useUpdateTask(): UseTaskMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (task: Task) => {
    try {
      setLoading(true);
      setError(undefined);
      const updatedTask = await projectsApi.updateTask(task);
      // In a real implementation, you might update the cache here
      console.log("Updated task:", updatedTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useDeleteTask(): UseTaskMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (task: Task) => {
    try {
      setLoading(true);
      setError(undefined);
      await projectsApi.deleteTask(task.id);
      // In a real implementation, you might update the cache here
      console.log("Deleted task:", task.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}
