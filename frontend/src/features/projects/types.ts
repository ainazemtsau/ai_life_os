// Types for the Projects and Tasks feature module

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
