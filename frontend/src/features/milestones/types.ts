// Types for the Milestones feature module

export interface Milestone {
  id: string; // UUID
  title: string;
  goal_id: string; // References a Goal
  due?: string; // RFC 3339 timestamp (optional)
  status: "todo" | "doing" | "done" | "blocked"; // Unified status enum
  demo_criterion: string; // Description of what constitutes completion
  blocking: boolean; // Whether this milestone blocks other items
  created_at: string; // RFC 3339 timestamp
  updated_at: string; // RFC 3339 timestamp
}
