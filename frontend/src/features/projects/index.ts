// Public API for frontend.projects module
// This is the main entry point for consumers of this module

export { ProjectsList } from "./ProjectsList";
export { ProjectForm } from "./ProjectForm";
export { TasksList } from "./TasksList";
export { TaskForm } from "./TaskForm";
export { DependencySelector } from "./DependencySelector";
export {
  useProjects,
  useTasks,
  useCreateProject,
  useUpdateProject,
  useDeleteProject,
  useCreateTask,
  useUpdateTask,
  useDeleteTask,
} from "./hooks";
export type { Project, Task } from "./types";
