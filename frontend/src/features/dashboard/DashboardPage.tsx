/**
 * Dashboard Page Component
 * Module: frontend.dashboard
 * Version: 0.1.0
 */

import * as React from "react";

import Link from "next/link";

import type { DashboardPageProps } from "@/contracts/dashboard";
import * as design from "@/features/design";

/**
 * Main dashboard page component
 * Displays greeting, welcome message, and navigation to Goals
 */
export const DashboardPage: React.FC<DashboardPageProps> = ({ className }) => {
  return (
    <div className={design.cn("container mx-auto px-4 py-8", className)}>
      <div className="mx-auto max-w-4xl space-y-8">
        {/* Greeting Section */}
        <div>
          <h1 className="mb-4 text-4xl font-bold">Welcome to AI Life OS</h1>
        </div>

        {/* Placeholder Information */}
        <design.Card>
          <design.CardHeader>
            <design.CardTitle>Your Personal Life Management System</design.CardTitle>
            <design.CardDescription>
              AI Life OS helps you organize, track, and achieve your goals with intelligent
              assistance.
            </design.CardDescription>
          </design.CardHeader>
          <design.CardContent>
            <div className="space-y-4">
              <p className="text-muted-foreground">
                This is the central hub for managing your personal goals and tasks. From here, you
                can access all the features designed to help you stay productive and focused.
              </p>
              <div>
                <h3 className="mb-2 font-semibold">Available Features:</h3>
                <ul className="list-inside list-disc space-y-1 text-muted-foreground">
                  <li>Goals Management - Track and organize your objectives</li>
                </ul>
              </div>
              <div>
                <h3 className="mb-2 font-semibold">Upcoming Features:</h3>
                <ul className="list-inside list-disc space-y-1 text-muted-foreground">
                  <li>Task Tracking - Break down goals into actionable tasks</li>
                  <li>Progress Analytics - Visualize your achievements</li>
                  <li>AI-Powered Insights - Get personalized recommendations</li>
                </ul>
              </div>
            </div>
          </design.CardContent>
        </design.Card>

        {/* Navigation to Goals */}
        <design.Card>
          <design.CardHeader>
            <design.CardTitle>Quick Actions</design.CardTitle>
          </design.CardHeader>
          <design.CardContent>
            <Link href="/goals">
              <design.Button className="w-full sm:w-auto">Go to Goals</design.Button>
            </Link>
          </design.CardContent>
        </design.Card>
      </div>
    </div>
  );
};
