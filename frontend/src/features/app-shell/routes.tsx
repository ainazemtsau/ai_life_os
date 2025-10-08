/**
 * Route Components
 * Module: frontend.app-shell
 * Version: 0.1.0
 *
 * These components wrap feature module pages for use in Next.js App Router
 */

"use client";

import * as React from "react";

import * as dashboard from "@/features/dashboard";
import * as goals from "@/features/goals";
import * as milestones from "@/features/milestones";
import * as projects from "@/features/projects";

/**
 * Dashboard route component
 * Wraps DashboardPage from frontend.dashboard module
 */
export const DashboardRoute: React.FC = () => {
  return <dashboard.DashboardPage />;
};

/**
 * Goals route component
 * Wraps GoalsPage from frontend.goals module
 */
export const GoalsRoute: React.FC = () => {
  return (
    <main className="min-h-screen bg-background p-6">
      <goals.GoalList />
    </main>
  );
};

/**
 * Milestones route component
 * Wraps MilestonesList from frontend.milestones module
 */
export const MilestonesRoute: React.FC = () => {
  return (
    <main className="min-h-screen bg-background p-6">
      <milestones.MilestonesList />
    </main>
  );
};

/**
 * Projects route component
 * Wraps ProjectsList from frontend.projects module
 */
export const ProjectsRoute: React.FC = () => {
  return (
    <main className="min-h-screen bg-background p-6">
      <projects.ProjectsList />
    </main>
  );
};

/**
 * Tasks route component
 * Wraps TasksList from frontend.projects module
 */
export const TasksRoute: React.FC = () => {
  return (
    <main className="min-h-screen bg-background p-6">
      <projects.TasksList />
    </main>
  );
};
