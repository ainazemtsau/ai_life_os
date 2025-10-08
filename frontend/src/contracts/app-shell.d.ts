/** Public contract — frontend.app-shell
 *  Version: 0.1.0
 *  This file defines the public TypeScript surface for the module.
 */

import type * as React from "react";

/**
 * Root application layout component props
 */
export interface AppLayoutProps {
  /** Child components to render within the layout */
  children: React.ReactNode;
  /** Optional className for additional styling */
  className?: string;
}

/**
 * Root application layout component
 * Provides consistent theme and structure across all pages
 */
export const AppLayout: React.FC<AppLayoutProps>;

/**
 * Dashboard route component
 * Wraps DashboardPage from frontend.dashboard module
 */
export const DashboardRoute: React.FC;

/**
 * Goals route component
 * Wraps GoalsPage from frontend.goals module
 */
export const GoalsRoute: React.FC;

/**
 * Milestones route component
 * Wraps MilestonesList from frontend.milestones module
 */
export const MilestonesRoute: React.FC;

/**
 * Projects route component
 * Wraps ProjectsList from frontend.projects module
 */
export const ProjectsRoute: React.FC;

/**
 * Tasks route component
 * Wraps TasksList from frontend.projects module
 */
export const TasksRoute: React.FC;
