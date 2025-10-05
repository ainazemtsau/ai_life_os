/**
 * SWR hook for fetching a single goal by ID
 */

import useSWR from 'swr';
import { goalsApi } from '../lib/api-client';
import type { UseGoalResult } from '../types';

export function useGoal(id: string): UseGoalResult {
  const { data, error, isLoading, mutate } = useSWR(
    id ? `/api/goals/${id}` : null,
    () => goalsApi.getGoal(id),
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  );

  return {
    goal: data || null,
    isLoading,
    error,
    mutate,
  };
}
