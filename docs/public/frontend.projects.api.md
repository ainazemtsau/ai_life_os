# Public API — frontend.projects
Version: 0.2.0

## Overview
Projects and Tasks UI module. Provides list pages, CRUD forms, dependency selectors, and API client hooks.

This module enables users to manage projects and tasks with support for dependencies. It includes UI components for displaying, creating, editing and deleting projects and tasks, along with hooks for interacting with the backend API. Dependency management follows DAG (Directed Acyclic Graph) validation to prevent circular dependencies.

## Exports
- `ProjectsList` - Component to display a list of projects in a table format
- `ProjectForm` - Component to create or edit a project with fields for title, goal selection, status, priority, risk, scope, and dependencies
- `TasksList` - Component to display a list of tasks in a table format
- `TaskForm` - Component to create or edit a task with fields for title, project selection, status, size, energy, continuity, clarity, risk, and dependencies
- `DependencySelector` - Component for selecting dependencies with filtering to ensure dependencies are within the same goal (for projects) or same project (for tasks)
- `useProjects` - Hook to fetch list of projects, with optional goal filtering
- `useTasks` - Hook to fetch list of tasks, with optional project filtering
- `useCreateProject` - Hook to create a new project
- `useUpdateProject` - Hook to update an existing project
- `useDeleteProject` - Hook to delete a project
- `useCreateTask` - Hook to create a new task
- `useUpdateTask` - Hook to update an existing task
- `useDeleteTask` - Hook to delete a task
- `Project` - Type definition for the Project entity
- `Task` - Type definition for the Task entity

## Types
Contract: frontend/src/contracts/projects.d.ts

### Project Type
The Project type contains the following properties:
- `id`: string - Unique identifier for the project (UUID)
- `title`: string - Title of the project
- `goal_id`: string (optional) - Reference to the associated goal
- `status`: 'todo' | 'doing' | 'done' | 'blocked' - Current status of the project
- `priority`: 'low' | 'medium' | 'high' | 'critical' - Priority level of the project
- `risk`: 'low' | 'medium' | 'high' - Risk level of the project
- `scope`: string (optional) - Description of the project's scope
- `dependencies`: string[] - Array of Project IDs within the same Goal
- `created_at`: string - Creation timestamp in RFC 3339 format
- `updated_at`: string - Last update timestamp in RFC 3339 format

### Task Type
The Task type contains the following properties:
- `id`: string - Unique identifier for the task (UUID)
- `title`: string - Title of the task
- `project_id`: string - Reference to the associated project
- `status`: 'todo' | 'doing' | 'done' | 'blocked' - Current status of the task
- `size`: 'tiny' | 'small' | 'medium' | 'large' | 'xlarge' - Size of the task
- `energy`: 'low' | 'medium' | 'high' - Energy required for the task
- `continuity`: 'discrete' | 'recurring' - Whether the task is discrete or recurring
- `clarity`: 'unclear' | 'fuzzy' | 'clear' - Clarity of the task requirements
- `risk`: 'low' | 'medium' | 'high' - Risk level of the task
- `dependencies`: string[] - Array of Task IDs within the same Project
- `created_at`: string - Creation timestamp in RFC 3339 format
- `updated_at`: string - Last update timestamp in RFC 3339 format

## Usage
```ts
// public surface import
import * as projects from '@/features/projects'

// Example: Using the ProjectsList component
<projects.ProjectsList 
  onProjectEdit={handleEdit} 
  onProjectDelete={handleDelete} 
/>

// Example: Using the ProjectForm component
<projects.ProjectForm 
  onSubmit={handleSubmit} 
  onCancel={handleCancel} 
  goals={availableGoals} 
  projects={availableProjects} 
/>

// Example: Using the TasksList component
<projects.TasksList 
  onTaskEdit={handleEdit} 
  onTaskDelete={handleDelete} 
/>

// Example: Using the TaskForm component
<projects.TaskForm 
  onSubmit={handleSubmit} 
  onCancel={handleCancel} 
  projects={availableProjects} 
  tasks={availableTasks} 
/>

// Example: Using the hooks
const { projects, loading, error } = projects.useProjects();
const { tasks, loading, error } = projects.useTasks();
const { mutate: createProject } = projects.useCreateProject();
const { mutate: updateProject } = projects.useUpdateProject();
const { mutate: deleteProject } = projects.useDeleteProject();
const { mutate: createTask } = projects.useCreateTask();
const { mutate: updateTask } = projects.useUpdateTask();
const { mutate: deleteTask } = projects.useDeleteTask();
```

## Dependencies
- `frontend.design` - Used for UI components and styling
- `backend.projects` - Provides the API contract for project and task operations

## Versioning
- 0.1.0 — Initial stub
- 0.2.0 — Added Projects and Tasks UI components with dependency management
