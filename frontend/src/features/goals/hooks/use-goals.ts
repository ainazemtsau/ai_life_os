/**
 * SWR hook for fetching goals list with caching and revalidation
 */

import useSWR from "swr";

import { goalsApi } from "../lib/api-client";
import type { Goal, UseGoalsResult } from "../types";

export function useGoals(filter?: "all" | "active" | "done"): UseGoalsResult {
  const status = filter === "all" ? undefined : filter;
  const key = status ? `/api/goals?status=${status}` : "/api/goals";
  const fetcher = async () => await goalsApi.listGoals(status);

  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { data, error, isLoading, mutate } = useSWR<{ goals: Goal[] }>(key, fetcher, {
    revalidateOnFocus: true,
    revalidateOnReconnect: true,
  });

  const handleMutate = () => {
    mutate().catch((err: unknown) => {
      console.error("Failed to mutate goals:", err);
    });
  };

  return {
    goals: data?.goals,
    isLoading,
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    error,
    mutate: handleMutate,
  };
}
