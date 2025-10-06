/**
 * Root Application Layout Component
 * Module: frontend.app-shell
 * Version: 0.1.0
 */

import * as React from "react";

import type { AppLayoutProps } from "@/contracts/app-shell";
import * as design from "@/features/design";

/**
 * Root application layout component
 * Provides consistent theme and structure across all pages
 */
export const AppLayout: React.FC<AppLayoutProps> = ({ children, className }) => {
  return (
    <div className={design.cn("dark min-h-screen bg-background text-foreground", className)}>
      {children}
    </div>
  );
};
