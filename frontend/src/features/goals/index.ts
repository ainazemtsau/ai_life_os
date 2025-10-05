// Re-export all components and hooks
export { GoalList } from './components/goal-list';
export { GoalForm } from './components/goal-form';
export { GoalItem } from './components/goal-item';

export { useGoals } from './hooks/use-goals';
export { useGoal } from './hooks/use-goal';
export { useGoalMutations } from './hooks/use-goal-mutations';

// Re-export types
export type {
  Goal,
  GoalCreateInput,
  GoalUpdateInput,
  GoalListProps,
  GoalFormProps,
  GoalItemProps,
  UseGoalsResult,
  UseGoalResult,
  UseGoalMutationsResult,
} from './types';
