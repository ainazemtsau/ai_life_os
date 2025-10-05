/**
 * GoalItem - Single goal row with inline actions
 */

import { Button } from '@/features/design';
import { cn } from '@/features/design';
import type { GoalItemProps } from '../types';

export function GoalItem({
  goal,
  onToggle,
  onEdit,
  onDelete,
  className,
}: GoalItemProps) {
  return (
    <div
      className={cn(
        'flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-accent/50',
        className
      )}
    >
      {/* Checkbox */}
      <input
        type="checkbox"
        checked={goal.isDone}
        onChange={(e) => onToggle(goal.id, e.target.checked)}
        className="h-4 w-4 rounded border-gray-300"
        aria-label={`Mark "${goal.title}" as ${goal.isDone ? 'incomplete' : 'complete'}`}
      />

      {/* Title */}
      <span
        className={cn(
          'flex-1 text-sm',
          goal.isDone && 'text-muted-foreground line-through'
        )}
      >
        {goal.title}
      </span>

      {/* Actions */}
      <div className="flex gap-2">
        <Button
          size="sm"
          variant="ghost"
          onClick={() => onEdit(goal)}
          aria-label={`Edit goal "${goal.title}"`}
        >
          Edit
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => onDelete(goal.id)}
          aria-label={`Delete goal "${goal.title}"`}
        >
          Delete
        </Button>
      </div>
    </div>
  );
}
