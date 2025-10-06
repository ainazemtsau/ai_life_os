/**
 * GoalForm - Create/edit goal form with validation
 */

"use client";

import { useState } from "react";

import { Button, Input, Label } from "@/features/design";
import { cn } from "@/features/design";

import { useGoalMutations } from "../hooks/use-goal-mutations";
import type { GoalFormProps } from "../types";

const MAX_CHARS = 255;

const validateTitle = (value: string): string | null => {
  if (!value.trim()) return "Title cannot be empty";
  if (value.length > MAX_CHARS) return `Title cannot exceed ${MAX_CHARS} characters`;
  return null;
};

const getCharCountColor = (count: number): string => {
  return count > MAX_CHARS * 0.9 ? "text-destructive" : "text-muted-foreground";
};

const getButtonText = (isMutating: boolean, isEdit: boolean): string => {
  if (isMutating) return "Saving...";
  return isEdit ? "Update" : "Create";
};

export function GoalForm({ goal, onSave, onCancel, className }: GoalFormProps) {
  const [title, setTitle] = useState(goal?.title || "");
  const [error, setError] = useState<string | null>(null);
  const { createGoal, updateGoal, isMutating } = useGoalMutations();

  const isEdit = !!goal;

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
    setError(null);
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
      const result = isEdit ? await updateGoal(goal.id, { title }) : await createGoal({ title });
      onSave(result);
      if (!isEdit) setTitle("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save goal");
    }
  };

  return (
    <form onSubmit={handleSubmit} className={cn("space-y-4", className)}>
      <div className="space-y-2">
        <Label htmlFor="goal-title">{isEdit ? "Edit Goal" : "New Goal"}</Label>
        <Input
          id="goal-title"
          type="text"
          value={title}
          onChange={handleInputChange}
          placeholder="Enter goal title..."
          error={!!error}
          disabled={isMutating}
          maxLength={MAX_CHARS}
          aria-describedby={error ? "goal-error" : "goal-char-count"}
        />

        <p id="goal-char-count" className={cn("text-xs", getCharCountColor(title.length))}>
          {title.length} / {MAX_CHARS}
        </p>

        {error && (
          <p id="goal-error" className="text-sm text-destructive">
            {error}
          </p>
        )}
      </div>

      <div className="flex gap-2">
        <Button type="submit" disabled={isMutating || !title.trim()}>
          {getButtonText(isMutating, isEdit)}
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
