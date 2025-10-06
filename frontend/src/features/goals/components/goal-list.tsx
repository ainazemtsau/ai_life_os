/**
 * GoalList - Display goals with filtering and management
 */

"use client";

import { useState } from "react";

import { Button, Card, CardHeader, CardTitle, CardContent } from "@/features/design";

import { GoalForm } from "./goal-form";
import { GoalItem } from "./goal-item";
import { useGoalMutations } from "../hooks/use-goal-mutations";
import { useGoals } from "../hooks/use-goals";
import type { GoalListProps, Goal } from "../types";

const getEmptyMessage = (filter: "all" | "active" | "done"): string => {
  if (filter === "done") return "No completed goals yet";
  if (filter === "active") return "No active goals";
  return "No goals yet. Create your first one!";
};

const ErrorDisplay = ({ message, className }: { message: string; className?: string }) => (
  <Card className={className}>
    <CardContent className="pt-6">
      <p className="text-sm text-destructive">Error loading goals: {message}</p>
    </CardContent>
  </Card>
);

const GoalsContent = ({
  goals,
  isLoading,
  filter,
  editingGoal,
  onToggle,
  onEdit,
  onDelete,
  onFormClose,
}: {
  goals: Goal[] | undefined;
  isLoading: boolean;
  filter: "all" | "active" | "done";
  editingGoal: Goal | null;
  onToggle: (id: string, isDone: boolean) => Promise<void>;
  onEdit: (goal: Goal) => void;
  onDelete: (id: string) => Promise<void>;
  onFormClose: () => void;
}) => {
  if (isLoading) return <p className="text-sm text-muted-foreground">Loading goals...</p>;
  if (!goals || goals.length === 0)
    return <p className="text-sm text-muted-foreground">{getEmptyMessage(filter)}</p>;

  return (
    <div className="space-y-2">
      {goals.map((goal) =>
        editingGoal?.id === goal.id ? (
          <GoalForm
            key={goal.id}
            goal={goal}
            onSave={onFormClose}
            onCancel={onFormClose}
            className="border-b pb-2 last:border-0"
          />
        ) : (
          <GoalItem
            key={goal.id}
            goal={goal}
            onToggle={onToggle}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ),
      )}
    </div>
  );
};

export function GoalList({ filter = "all", className }: GoalListProps) {
  const { goals, isLoading, error } = useGoals(filter);
  const { updateGoal, deleteGoal } = useGoalMutations();
  const [editingGoal, setEditingGoal] = useState<Goal | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  const handleToggle = async (id: string, isDone: boolean) => {
    try {
      await updateGoal(id, { isDone });
    } catch (err) {
      console.error("Failed to toggle goal:", err);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this goal?")) return;
    try {
      await deleteGoal(id);
    } catch (err) {
      console.error("Failed to delete goal:", err);
    }
  };

  if (error) {
    return className ? (
      <ErrorDisplay message={error.message} className={className} />
    ) : (
      <ErrorDisplay message={error.message} />
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Goals</CardTitle>
          <Button
            size="sm"
            onClick={() => {
              setIsCreating(true);
              setEditingGoal(null);
            }}
            disabled={isCreating}
          >
            New Goal
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {isCreating && (
          <GoalForm
            onSave={() => {
              setEditingGoal(null);
              setIsCreating(false);
            }}
            onCancel={() => {
              setEditingGoal(null);
              setIsCreating(false);
            }}
            className="border-b pb-4"
          />
        )}

        <GoalsContent
          goals={goals}
          isLoading={isLoading}
          filter={filter}
          editingGoal={editingGoal}
          onToggle={handleToggle}
          onEdit={(goal) => {
            setEditingGoal(goal);
            setIsCreating(false);
          }}
          onDelete={handleDelete}
          onFormClose={() => {
            setEditingGoal(null);
            setIsCreating(false);
          }}
        />
      </CardContent>
    </Card>
  );
}
