// Public API for frontend.milestones module
// This is the main entry point for consumers of this module

export { MilestonesList } from "./MilestonesList";
export { MilestoneForm } from "./MilestoneForm";
export { useMilestones, useCreateMilestone, useUpdateMilestone, useDeleteMilestone } from "./hooks";
export type { Milestone } from "./types";
