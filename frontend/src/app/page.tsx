'use client';

import { GoalList } from '@/features/goals';

export default function Page() {
  return (
    <main className="min-h-screen bg-background p-6">
      <div className="mx-auto max-w-4xl space-y-6">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">AI Life OS</h1>
          <p className="text-muted-foreground">
            Manage your personal goals and track your progress
          </p>
        </div>

        <GoalList />
      </div>
    </main>
  );
}
