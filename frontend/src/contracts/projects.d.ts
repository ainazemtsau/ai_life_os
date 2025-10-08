// Type contract for frontend.projects module
// Public API surface - changes here require SemVer major update

// Adjust import path as needed
import type { Goal } from "@/features/goals/contracts/goals.d"; // Adjust import path as needed

// Define the Project type based on backend schema
export interface Project {
  id: string; // UUID
  title: string;
  goal_id?: string; // References a Goal (optional)
  status: "todo" | "doing" | "done" | "blocked";
  priority: "low" | "medium" | "high" | "critical";
  risk: "low" | "medium" | "high";
  scope?: string; // Description of the project's scope
  dependencies: string[]; // Array of Project IDs within the same Goal
  created_at: string; // RFC 3339 timestamp
  updated_at: string; // RFC 3339 timestamp
}

// Define the Task type based on backend schema
export interface Task {
  id: string; // UUID
  title: string;
  project_id: string; // References a Project
  status: "todo" | "doing" | "done" | "blocked";
  size: "tiny" | "small" | "medium" | "large" | "xlarge";
  energy: "low" | "medium" | "high";
  continuity: "discrete" | "recurring";
  clarity: "unclear" | "fuzzy" | "clear";
  risk: "low" | "medium" | "high";
  dependencies: string[]; // Array of Task IDs within the same Project
  created_at: string; // RFC 3339 timestamp
  updated_at: string; // RFC 3339 timestamp
}

// Props for the ProjectsList component
export interface ProjectsListProps {
  onProjectEdit?: (project: Project) => void;
  onProjectDelete?: (project: Project) => void;
  filterByGoal?: string; // Filter by goal ID
}

// Props for the TasksList component
export interface TasksListProps {
  onTaskEdit?: (task: Task) => void;
  onTaskDelete?: (task: Task) => void;
  filterByProject?: string; // Filter by project ID
}

// Props for the ProjectForm component
export interface ProjectFormProps {
  project?: Project; // If provided, form is in edit mode
  onSubmit: (project: Project) => void;
  onCancel: () => void;
  goals: Goal[]; // Available goals for the goal selector
  projects: Project[]; // Available projects for the dependency selector (same goal)
}

// Props for the TaskForm component
export interface TaskFormProps {
  task?: Task; // If provided, form is in edit mode
  onSubmit: (task: Task) => void;
  onCancel: () => void;
  projects: Project[]; // Available projects for the project selector
  tasks: Task[]; // Available tasks for the dependency selector (same project)
}

// Props for the DependencySelector component
export interface DependencySelectorProps {
  selectedDependencies: string[];
  availableDependencies: Array<{ id: string; title: string }>;
  onChange: (selectedIds: string[]) => void;
  label?: string;
}

// Return type for useProjects hook
export interface UseProjectsReturn {
  projects: Project[];
  loading: boolean;
  error?: string;
  refetch: () => void;
}

// Return type for useTasks hook
export interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error?: string;
  refetch: () => void;
}

// Return type for project/task mutation hooks
export interface UseProjectMutationReturn {
  mutate: (project: Project) => Promise<void>;
  loading: boolean;
  error?: string;
}

export interface UseTaskMutationReturn {
  mutate: (task: Task) => Promise<void>;
  loading: boolean;
  error?: string;
}

// Public components
export const ProjectsList: React.ComponentType<ProjectsListProps>;
export const ProjectForm: React.ComponentType<ProjectFormProps>;
export const TasksList: React.ComponentType<TasksListProps>;
export const TaskForm: React.ComponentType<TaskFormProps>;
export const DependencySelector: React.ComponentType<DependencySelectorProps>;

// Public hooks
export function useProjects(goalId?: string): UseProjectsReturn;
export function useTasks(projectId?: string): UseTasksReturn;
export function useCreateProject(): UseProjectMutationReturn;
export function useUpdateProject(): UseProjectMutationReturn;
export function useDeleteProject(): UseProjectMutationReturn;
export function useCreateTask(): UseTaskMutationReturn;
export function useUpdateTask(): UseTaskMutationReturn;
export function useDeleteTask(): UseTaskMutationReturn;
