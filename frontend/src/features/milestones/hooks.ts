import { useState, useEffect, useCallback } from "react";

import type { Milestone } from "@/features/milestones/types"; // Assuming a types file exists or will be created

// Mock API service - this would connect to your actual backend API
const milestoneApi = {
  getMilestones: async (goalId?: string): Promise<Milestone[]> => {
    // This would be an actual API call in a real implementation
    // For now, returning mock data
    console.log("Fetching milestones", goalId);
    return Promise.resolve([]);
  },

  createMilestone: async (
    milestone: Omit<Milestone, "id" | "created_at" | "updated_at">,
  ): Promise<Milestone> => {
    // This would be an actual API call in a real implementation
    console.log("Creating milestone", milestone);
    return Promise.resolve({
      ...milestone,
      id: "new-id", // This would come from the API response
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  },

  updateMilestone: async (milestone: Milestone): Promise<Milestone> => {
    // This would be an actual API call in a real implementation
    console.log("Updating milestone", milestone);
    return Promise.resolve(milestone);
  },

  deleteMilestone: async (id: string): Promise<void> => {
    // This would be an actual API call in a real implementation
    console.log("Deleting milestone", id);
    return Promise.resolve();
  },
};

// Return type for useMilestones hook
interface UseMilestonesReturn {
  milestones: Milestone[];
  loading: boolean;
  error?: string;
  refetch: () => void;
}

// Return type for milestone mutation hooks
interface UseMilestoneMutationReturn {
  mutate: (milestone: Milestone) => Promise<void>;
  loading: boolean;
  error?: string;
}

export function useMilestones(goalId?: string): UseMilestonesReturn {
  const [milestones, setMilestones] = useState<Milestone[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | undefined>(undefined);

  const fetchMilestones = useCallback(async () => {
    try {
      setLoading(true);
      setError(undefined);
      const data = await milestoneApi.getMilestones(goalId);
      setMilestones(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch milestones");
    } finally {
      setLoading(false);
    }
  }, [goalId]);

  useEffect(() => {
    fetchMilestones().catch((err) => {
      console.error("Error fetching milestones:", err);
    });
  }, [fetchMilestones]);

  const refetch = useCallback(() => {
    fetchMilestones().catch((err) => {
      console.error("Error fetching milestones:", err);
    });
  }, [fetchMilestones]);

  return error ? { milestones, loading, error, refetch } : { milestones, loading, refetch };
}

export function useCreateMilestone(): UseMilestoneMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (milestone: Milestone) => {
    try {
      setLoading(true);
      setError(undefined);
      const newMilestone = await milestoneApi.createMilestone(milestone);
      // In a real implementation, you might update the cache here
      console.log("Created milestone:", newMilestone);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create milestone");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useUpdateMilestone(): UseMilestoneMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (milestone: Milestone) => {
    try {
      setLoading(true);
      setError(undefined);
      const updatedMilestone = await milestoneApi.updateMilestone(milestone);
      // In a real implementation, you might update the cache here
      console.log("Updated milestone:", updatedMilestone);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update milestone");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}

export function useDeleteMilestone(): UseMilestoneMutationReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (milestone: Milestone) => {
    try {
      setLoading(true);
      setError(undefined);
      await milestoneApi.deleteMilestone(milestone.id);
      // In a real implementation, you might update the cache here
      console.log("Deleted milestone:", milestone.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete milestone");
    } finally {
      setLoading(false);
    }
  };

  return error ? { mutate, loading, error } : { mutate, loading };
}
