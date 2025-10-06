/**
 * Hook for goal mutations with optimistic updates
 */

import { useState } from "react";

import { useSWRConfig } from "swr";

import { goalsApi } from "../lib/api-client";
import type { Goal, GoalCreateInput, GoalUpdateInput, UseGoalMutationsResult } from "../types";

const GOALS_API_PREFIX = "/api/goals";

const isGoalsKey = (key: unknown): boolean => {
  return typeof key === "string" && key.startsWith(GOALS_API_PREFIX);
};

export function useGoalMutations(): UseGoalMutationsResult {
  const { mutate } = useSWRConfig();
  const [isMutating, setIsMutating] = useState(false);

  const createGoal = async (input: GoalCreateInput): Promise<Goal> => {
    setIsMutating(true);
    try {
      const newGoal = await goalsApi.createGoal(input);
      await mutate(isGoalsKey);
      return newGoal;
    } finally {
      setIsMutating(false);
    }
  };

  const updateGoal = async (id: string, input: GoalUpdateInput): Promise<Goal> => {
    setIsMutating(true);
    try {
      const updatedGoal = await goalsApi.updateGoal(id, input);
      await mutate(`${GOALS_API_PREFIX}/${id}`);
      await mutate(isGoalsKey);
      return updatedGoal;
    } finally {
      setIsMutating(false);
    }
  };

  const deleteGoal = async (id: string): Promise<void> => {
    setIsMutating(true);
    try {
      await goalsApi.deleteGoal(id);
      await mutate(`${GOALS_API_PREFIX}/${id}`, undefined, { revalidate: false });
      await mutate(isGoalsKey);
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
