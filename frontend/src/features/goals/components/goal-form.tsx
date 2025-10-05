/**
 * GoalForm - Create/edit goal form with validation
 */

'use client';

import { useState } from 'react';
import { Button, Input, Label } from '@/features/design';
import { cn } from '@/features/design';
import type { GoalFormProps } from '../types';
import { useGoalMutations } from '../hooks/use-goal-mutations';

export function GoalForm({ goal, onSave, onCancel, className }: GoalFormProps) {
  const [title, setTitle] = useState(goal?.title || '');
  const [error, setError] = useState<string | null>(null);
  const { createGoal, updateGoal, isMutating } = useGoalMutations();

  const isEdit = !!goal;
  const charCount = title.length;
  const maxChars = 255;

  const validateTitle = (value: string): string | null => {
    if (!value.trim()) {
      return 'Title cannot be empty';
    }
    if (value.length > maxChars) {
      return `Title cannot exceed ${maxChars} characters`;
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationError = validateTitle(title);
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setError(null);
      const result = isEdit
        ? await updateGoal(goal.id, { title })
        : await createGoal({ title });

      onSave(result);
      if (!isEdit) {
        setTitle(''); // Clear form after create
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save goal');
    }
  };

  return (
    <form onSubmit={handleSubmit} className={cn('space-y-4', className)}>
      <div className="space-y-2">
        <Label htmlFor="goal-title">
          {isEdit ? 'Edit Goal' : 'New Goal'}
        </Label>
        <Input
          id="goal-title"
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            setError(null);
          }}
          placeholder="Enter goal title..."
          error={!!error}
          disabled={isMutating}
          maxLength={maxChars}
          aria-describedby={error ? 'goal-error' : 'goal-char-count'}
        />

        {/* Character counter */}
        <p
          id="goal-char-count"
          className={cn(
            'text-xs',
            charCount > maxChars * 0.9 ? 'text-destructive' : 'text-muted-foreground'
          )}
        >
          {charCount} / {maxChars}
        </p>

        {/* Error message */}
        {error && (
          <p id="goal-error" className="text-sm text-destructive">
            {error}
          </p>
        )}
      </div>

      <div className="flex gap-2">
        <Button type="submit" disabled={isMutating || !title.trim()}>
          {isMutating ? 'Saving...' : isEdit ? 'Update' : 'Create'}
        </Button>
        {isEdit && (
          <Button type="button" variant="outline" onClick={onCancel} disabled={isMutating}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}
