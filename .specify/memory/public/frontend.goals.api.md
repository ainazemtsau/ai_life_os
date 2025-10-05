# Public API — frontend.goals
Version: 0.1.0

## Overview
React components and hooks for managing personal goals in the UI. Provides CRUD operations, filtering by completion status, and real-time state management via SWR. Consumes the backend.goals REST API and uses frontend.design components for consistent UX.

## Exports
### Components
- `GoalList` - Display list of goals with filtering (`GoalListProps`)
- `GoalForm` - Create/edit form with validation (`GoalFormProps`)
- `GoalItem` - Single goal row with inline actions (`GoalItemProps`)

### Hooks (SWR-based)
- `useGoals(filter?: 'all' | 'active' | 'done')` - Fetch goals list with caching/revalidation
- `useGoal(id: string)` - Fetch single goal by ID
- `useGoalMutations()` - Mutation functions (createGoal, updateGoal, deleteGoal) with optimistic updates

## Types
Contract: `frontend/src/contracts/goals.d.ts`

**Key types:**
- `Goal` - {id: string, title: string, isDone: boolean, dateCreated: string, dateUpdated: string}
- `GoalCreateInput` - {title: string (1-255 chars)}
- `GoalUpdateInput` - {title?: string, isDone?: boolean}
- `ApiError` - {detail: string, type?: string, status?: number}

**Component prop types:**
- `GoalListProps`, `GoalFormProps`, `GoalItemProps`

**Hook return types:**
- `UseGoalsResult`, `UseGoalResult`, `UseGoalMutationsResult`

## Usage
```ts
// Import components
import { GoalList, GoalForm, GoalItem } from '@/features/goals';

// Import hooks
import { useGoals, useGoal, useGoalMutations } from '@/features/goals';

// Example: Goals page
function GoalsPage() {
  const { goals, isLoading, error } = useGoals('active');
  const { createGoal } = useGoalMutations();

  return (
    <div>
      <GoalForm onSave={(goal) => console.log('Created:', goal)} onCancel={() => {}} />
      <GoalList filter="active" />
    </div>
  );
}
```

## Stability
- exports: **experimental** (v0.1.0 - component APIs may evolve based on UX needs)
- types: **experimental** (TypeScript interfaces may refine)

## Dependencies
- **frontend.design** - Uses design system components (Button, Dialog, Input, etc.)
- **backend.goals** - Consumes REST API (HTTP only, no direct imports)
- External: React 19, SWR, Next.js 15

## Versioning
- **0.1.0** - Initial MVP release
- SemVer policy: MAJOR for breaking prop changes, MINOR for new components/optional props, PATCH for bug fixes

## Notes
- SWR provides automatic caching, revalidation on focus/reconnect
- Optimistic UI updates for instant feedback
- All components accept `className` prop for Tailwind styling
- Error handling: displays user-friendly messages, disables actions when backend unavailable
- Accessibility: follows Radix UI patterns for keyboard navigation and screen readers
