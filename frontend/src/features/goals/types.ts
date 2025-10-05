/**
 * Type definitions for goals feature module
 */

// ============================================================================
// Domain Types (from backend API)
// ============================================================================

export interface Goal {
  id: string;
  title: string;
  isDone: boolean;
  dateCreated: string;
  dateUpdated: string;
}

export interface GoalCreateInput {
  title: string;
}

export interface GoalUpdateInput {
  title?: string;
  isDone?: boolean;
}

export interface ApiError {
  detail: string;
  type?: string;
  status?: number;
}

// ============================================================================
// Component Prop Types
// ============================================================================

export interface GoalListProps {
  filter?: 'all' | 'active' | 'done';
  onGoalClick?: (goal: Goal) => void;
  className?: string;
}

export interface GoalFormProps {
  goal?: Goal;
  onSave: (goal: Goal) => void;
  onCancel: () => void;
  className?: string;
}

export interface GoalItemProps {
  goal: Goal;
  onToggle: (goalId: string, isDone: boolean) => void;
  onEdit: (goal: Goal) => void;
  onDelete: (goalId: string) => void;
  className?: string;
}

// ============================================================================
// Hook Return Types
// ============================================================================

export interface UseGoalsResult {
  goals: Goal[] | undefined;
  isLoading: boolean;
  error: Error | undefined;
  mutate: () => void;
}

export interface UseGoalResult {
  goal: Goal | null | undefined;
  isLoading: boolean;
  error: Error | undefined;
  mutate: () => void;
}

export interface UseGoalMutationsResult {
  createGoal: (input: GoalCreateInput) => Promise<Goal>;
  updateGoal: (id: string, input: GoalUpdateInput) => Promise<Goal>;
  deleteGoal: (id: string) => Promise<void>;
  isMutating: boolean;
}
