/**
 * SWR hook for fetching goals list with caching and revalidation
 */

import useSWR from 'swr';
import { goalsApi } from '../lib/api-client';
import type { UseGoalsResult } from '../types';

export function useGoals(filter?: 'all' | 'active' | 'done'): UseGoalsResult {
  const status = filter === 'all' ? undefined : filter;
  const key = status ? `/api/goals?status=${status}` : '/api/goals';

  const { data, error, isLoading, mutate } = useSWR(
    key,
    () => goalsApi.listGoals(status),
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  );

  return {
    goals: data?.goals,
    isLoading,
    error,
    mutate,
  };
}
