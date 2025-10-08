// Type contract for frontend.milestones module
// Public API surface - changes here require SemVer major update

// Adjust import path as needed
import type { Goal } from "@/features/goals/contracts/goals.d"; // Adjust import path as needed

// Define the Milestone type based on backend schema
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

// Props for the MilestonesList component
export interface MilestonesListProps {
  onMilestoneEdit?: (milestone: Milestone) => void;
  onMilestoneDelete?: (milestone: Milestone) => void;
  filterByGoal?: string; // Filter by goal ID
}

// Props for the MilestoneForm component
export interface MilestoneFormProps {
  milestone?: Milestone; // If provided, form is in edit mode
  onSubmit: (milestone: Milestone) => void;
  onCancel: () => void;
  goals: Goal[]; // Available goals for the goal selector
}

// Return type for useMilestones hook
export interface UseMilestonesReturn {
  milestones: Milestone[];
  loading: boolean;
  error?: string;
  refetch: () => void;
}

// Return type for milestone mutation hooks
export interface UseMilestoneMutationReturn {
  mutate: (milestone: Milestone) => Promise<void>;
  loading: boolean;
  error?: string;
}

// Public components
export const MilestonesList: React.ComponentType<MilestonesListProps>;
export const MilestoneForm: React.ComponentType<MilestoneFormProps>;

// Public hooks
export function useMilestones(goalId?: string): UseMilestonesReturn;
export function useCreateMilestone(): UseMilestoneMutationReturn;
export function useUpdateMilestone(): UseMilestoneMutationReturn;
export function useDeleteMilestone(): UseMilestoneMutationReturn;
