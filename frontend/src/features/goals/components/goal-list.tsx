/**
 * GoalList - Display goals with filtering and management
 */

'use client';

import { useState } from 'react';
import { Button, Card, CardHeader, CardTitle, CardContent } from '@/features/design';
import { cn } from '@/features/design';
import { GoalItem } from './goal-item';
import { GoalForm } from './goal-form';
import type { GoalListProps, Goal } from '../types';
import { useGoals } from '../hooks/use-goals';
import { useGoalMutations } from '../hooks/use-goal-mutations';

export function GoalList({ filter = 'all', className }: GoalListProps) {
  const { goals, isLoading, error } = useGoals(filter);
  const { updateGoal, deleteGoal } = useGoalMutations();
  const [editingGoal, setEditingGoal] = useState<Goal | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  const handleToggle = async (id: string, isDone: boolean) => {
    try {
      await updateGoal(id, { isDone });
    } catch (err) {
      console.error('Failed to toggle goal:', err);
    }
  };

  const handleEdit = (goal: Goal) => {
    setEditingGoal(goal);
    setIsCreating(false);
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this goal?')) {
      try {
        await deleteGoal(id);
      } catch (err) {
        console.error('Failed to delete goal:', err);
      }
    }
  };

  const handleSave = () => {
    setEditingGoal(null);
    setIsCreating(false);
  };

  const handleCancel = () => {
    setEditingGoal(null);
    setIsCreating(false);
  };

  if (error) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <p className="text-sm text-destructive">
            Error loading goals: {error.message}
          </p>
        </CardContent>
      </Card>
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
        {/* Create form */}
        {isCreating && (
          <GoalForm
            onSave={handleSave}
            onCancel={handleCancel}
            className="pb-4 border-b"
          />
        )}

        {/* Loading state */}
        {isLoading && (
          <p className="text-sm text-muted-foreground">Loading goals...</p>
        )}

        {/* Empty state */}
        {!isLoading && goals && goals.length === 0 && (
          <p className="text-sm text-muted-foreground">
            {filter === 'done'
              ? 'No completed goals yet'
              : filter === 'active'
              ? 'No active goals'
              : 'No goals yet. Create your first one!'}
          </p>
        )}

        {/* Goals list */}
        {!isLoading && goals && goals.length > 0 && (
          <div className="space-y-2">
            {goals.map((goal) =>
              editingGoal?.id === goal.id ? (
                <GoalForm
                  key={goal.id}
                  goal={goal}
                  onSave={handleSave}
                  onCancel={handleCancel}
                  className="pb-2 border-b last:border-0"
                />
              ) : (
                <GoalItem
                  key={goal.id}
                  goal={goal}
                  onToggle={handleToggle}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              )
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
