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
