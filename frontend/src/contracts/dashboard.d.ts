/** Public contract — frontend.dashboard
 *  Version: 0.1.0
 *  This file defines the public TypeScript surface for the module.
 */

import type * as React from "react";

/**
 * Dashboard page component props
 */
export interface DashboardPageProps {
  /** Optional className for styling customization */
  className?: string;
}

/**
 * Main dashboard page component
 * Displays greeting, welcome message, and navigation to Goals
 */
export const DashboardPage: React.FC<DashboardPageProps>;
