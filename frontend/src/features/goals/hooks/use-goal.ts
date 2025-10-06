/**
 * SWR hook for fetching a single goal by ID
 */

import useSWR from "swr";

import { goalsApi } from "../lib/api-client";
import type { Goal, UseGoalResult } from "../types";

export function useGoal(id: string): UseGoalResult {
  const fetcher = async () => await goalsApi.getGoal(id);

  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { data, error, isLoading, mutate } = useSWR<Goal>(id ? `/api/goals/${id}` : null, fetcher, {
    revalidateOnFocus: true,
    revalidateOnReconnect: true,
  });

  const handleMutate = () => {
    mutate().catch((err: unknown) => {
      console.error("Failed to mutate goal:", err);
    });
  };

  return {
    goal: data ?? null,
    isLoading,
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    error,
    mutate: handleMutate,
  };
}
