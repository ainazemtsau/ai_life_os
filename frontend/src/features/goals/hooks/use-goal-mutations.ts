/**
 * Hook for goal mutations with optimistic updates
 */

import { useState } from 'react';
import { useSWRConfig } from 'swr';
import { goalsApi } from '../lib/api-client';
import type { Goal, GoalCreateInput, GoalUpdateInput, UseGoalMutationsResult } from '../types';

export function useGoalMutations(): UseGoalMutationsResult {
  const { mutate } = useSWRConfig();
  const [isMutating, setIsMutating] = useState(false);

  const createGoal = async (input: GoalCreateInput): Promise<Goal> => {
    setIsMutating(true);
    try {
      const newGoal = await goalsApi.createGoal(input);

      // Invalidate all goals lists
      await mutate((key: unknown) => typeof key === 'string' && key.startsWith('/api/goals'));

      return newGoal;
    } finally {
      setIsMutating(false);
    }
  };

  const updateGoal = async (id: string, input: GoalUpdateInput): Promise<Goal> => {
    setIsMutating(true);
    try {
      const updatedGoal = await goalsApi.updateGoal(id, input);

      // Invalidate specific goal and lists
      await mutate(`/api/goals/${id}`);
      await mutate((key: unknown) => typeof key === 'string' && key.startsWith('/api/goals'));

      return updatedGoal;
    } finally {
      setIsMutating(false);
    }
  };

  const deleteGoal = async (id: string): Promise<void> => {
    setIsMutating(true);
    try {
      await goalsApi.deleteGoal(id);

      // Invalidate specific goal and lists
      await mutate(`/api/goals/${id}`, undefined, { revalidate: false });
      await mutate((key: unknown) => typeof key === 'string' && key.startsWith('/api/goals'));
    } finally {
      setIsMutating(false);
    }
  };

  return {
    createGoal,
    updateGoal,
    deleteGoal,
    isMutating,
  };
}
