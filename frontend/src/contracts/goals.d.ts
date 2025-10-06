/**
 * Goals Management Frontend API Contract
 * Version: 0.1.0
 *
 * TypeScript type definitions for Goals Management feature.
 * This contract defines the public surface for frontend.goals module.
 */

/**
 * Goal entity (domain model)
 */
export interface Goal {
  /** Unique identifier (UUID) */
  id: string;

  /** Goal title (1-255 characters, non-empty) */
  title: string;

  /** Completion status (false = active, true = done) */
  isDone: boolean;

  /** ISO 8601 timestamp when goal was created */
  dateCreated: string;

  /** ISO 8601 timestamp of last modification */
  dateUpdated: string;
}

/**
 * Input for creating a new goal
 */
export interface GoalCreateInput {
  /** Goal title (1-255 characters, non-empty after trim) */
  title: string;
}

/**
 * Input for updating an existing goal
 * At least one field must be provided
 */
export interface GoalUpdateInput {
  /** New goal title (1-255 characters, optional) */
  title?: string;

  /** New completion status (optional) */
  isDone?: boolean;
}

/**
 * Filter options for listing goals
 */
export type GoalFilterStatus = "all" | "active" | "done";

/**
 * API error response
 */
export interface ApiError {
  /** Human-readable error message */
  detail: string;

  /** Error type identifier (e.g., 'validation_error') */
  type?: string;

  /** HTTP status code */
  status?: number;
}

/**
 * Goals API client interface
 * This is the public contract for the frontend.goals module
 */
export interface GoalsApi {
  /**
   * List all goals, optionally filtered by completion status
   * Goals are sorted by: active first, then by date_updated DESC
   *
   * @param status - Filter by completion status ('all', 'active', 'done')
   * @returns Promise resolving to array of goals
   * @throws ApiError if request fails
   */
  listGoals(status?: GoalFilterStatus): Promise<Goal[]>;

  /**
   * Get a single goal by ID
   *
   * @param id - Goal UUID
   * @returns Promise resolving to goal, or null if not found
   * @throws ApiError if request fails (network error, server error)
   */
  getGoal(id: string): Promise<Goal | null>;

  /**
   * Create a new goal
   *
   * @param input - Goal creation data (title)
   * @returns Promise resolving to created goal
   * @throws ApiError if validation fails or request fails
   */
  createGoal(input: GoalCreateInput): Promise<Goal>;

  /**
   * Update an existing goal (title and/or completion status)
   *
   * @param id - Goal UUID
   * @param input - Fields to update (at least one required)
   * @returns Promise resolving to updated goal
   * @throws ApiError if goal not found, validation fails, or request fails
   */
  updateGoal(id: string, input: GoalUpdateInput): Promise<Goal>;

  /**
   * Delete a goal permanently
   *
   * @param id - Goal UUID
   * @returns Promise resolving to true if deleted, false if not found
   * @throws ApiError if request fails
   */
  deleteGoal(id: string): Promise<boolean>;
}

/**
 * React hooks for Goals feature (SWR-based)
 */

/**
 * SWR hook for fetching goals list
 */
export interface UseGoalsResult {
  /** Array of goals (undefined during initial load) */
  goals: Goal[] | undefined;

  /** Loading state (true during initial fetch) */
  isLoading: boolean;

  /** Error object if fetch failed */
  error: ApiError | undefined;

  /** Revalidate data manually */
  mutate: () => Promise<void>;
}

/**
 * SWR hook for fetching a single goal
 */
export interface UseGoalResult {
  /** Goal object (undefined during initial load, null if not found) */
  goal: Goal | null | undefined;

  /** Loading state (true during initial fetch) */
  isLoading: boolean;

  /** Error object if fetch failed */
  error: ApiError | undefined;

  /** Revalidate data manually */
  mutate: () => Promise<void>;
}

/**
 * Hook for goal mutations (create, update, delete)
 */
export interface UseGoalMutationsResult {
  /** Create a new goal with optimistic update */
  createGoal: (input: GoalCreateInput) => Promise<Goal>;

  /** Update a goal with optimistic update */
  updateGoal: (id: string, input: GoalUpdateInput) => Promise<Goal>;

  /** Delete a goal with optimistic update */
  deleteGoal: (id: string) => Promise<void>;

  /** True if any mutation is in progress */
  isMutating: boolean;
}

/**
 * React component props
 */

/**
 * Props for GoalList component
 */
export interface GoalListProps {
  /** Filter status (defaults to 'all') */
  filter?: GoalFilterStatus;

  /** Callback when goal is clicked (for detail view) */
  onGoalClick?: (goal: Goal) => void;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Props for GoalForm component (create/edit)
 */
export interface GoalFormProps {
  /** Goal to edit (undefined for create mode) */
  goal?: Goal;

  /** Callback when goal is saved */
  onSave: (goal: Goal) => void;

  /** Callback when form is cancelled */
  onCancel: () => void;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Props for GoalItem component
 */
export interface GoalItemProps {
  /** Goal to display */
  goal: Goal;

  /** Callback when completion status is toggled */
  onToggle: (id: string, isDone: boolean) => void;

  /** Callback when edit is requested */
  onEdit: (goal: Goal) => void;

  /** Callback when delete is requested */
  onDelete: (id: string) => void;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Public components exported by frontend.goals module
 */
export const GoalList: React.FC<GoalListProps>;
export const GoalForm: React.FC<GoalFormProps>;
export const GoalItem: React.FC<GoalItemProps>;

/**
 * Public hooks exported by frontend.goals module
 */
export function useGoals(filter?: GoalFilterStatus): UseGoalsResult;
export function useGoal(id: string): UseGoalResult;
export function useGoalMutations(): UseGoalMutationsResult;
