# Frontend Goals API Manifest

**Module**: `frontend.goals`
**Version**: 0.1.0 (MVP)
**Kind**: TypeScript
**Contract**: [goals.d.ts](./goals.d.ts)

## Overview
React components and hooks for managing personal goals. Provides UI for CRUD operations, filtering, and real-time state management via SWR.

## Public Surface

### Components

#### `GoalList`
Displays a list of goals with optional filtering.

**Props** (`GoalListProps`):
```typescript
{
  filter?: 'all' | 'active' | 'done';  // Default: 'all'
  onGoalClick?: (goal: Goal) => void;
  className?: string;
}
```

**Features**:
- Displays goals sorted by: active first, then by date_updated DESC
- Shows loading state during initial fetch
- Shows error message if backend unavailable
- Shows empty state if no goals match filter
- Handles optimistic updates for toggle/delete actions

**Usage**:
```tsx
import { GoalList } from '@/components/goals';

<GoalList filter="active" onGoalClick={(goal) => console.log(goal.id)} />
```

---

#### `GoalForm`
Form for creating or editing a goal.

**Props** (`GoalFormProps`):
```typescript
{
  goal?: Goal;                        // Undefined for create mode
  onSave: (goal: Goal) => void;
  onCancel: () => void;
  className?: string;
}
```

**Features**:
- Create mode (no `goal` prop): Empty form for new goal
- Edit mode (`goal` provided): Pre-filled form
- Client-side validation:
  - Title required (non-empty after trim)
  - Title max 255 characters
  - Character counter display
- Disables submit button while mutating
- Displays validation errors from API (422 responses)

**Usage**:
```tsx
import { GoalForm } from '@/components/goals';

// Create mode
<GoalForm onSave={(goal) => console.log('Created:', goal)} onCancel={() => {}} />

// Edit mode
<GoalForm goal={existingGoal} onSave={(goal) => console.log('Updated:', goal)} onCancel={() => {}} />
```

---

#### `GoalItem`
Single goal item with inline actions (toggle, edit, delete).

**Props** (`GoalItemProps`):
```typescript
{
  goal: Goal;
  onToggle: (id: string, isDone: boolean) => void;
  onEdit: (goal: Goal) => void;
  onDelete: (id: string) => void;
  className?: string;
}
```

**Features**:
- Checkbox for toggling completion status
- Visual distinction between active/done goals (styling)
- Edit button (opens edit form)
- Delete button with confirmation
- Optimistic updates for toggle action

**Usage**:
```tsx
import { GoalItem } from '@/components/goals';

<GoalItem
  goal={goal}
  onToggle={(id, isDone) => updateGoal(id, { isDone })}
  onEdit={(goal) => openEditModal(goal)}
  onDelete={(id) => deleteGoal(id)}
/>
```

---

### Hooks

#### `useGoals(filter?)`
Fetches list of goals with optional filtering (SWR-based).

**Parameters**:
- `filter?: 'all' | 'active' | 'done'` (default: `'all'`)

**Returns** (`UseGoalsResult`):
```typescript
{
  goals: Goal[] | undefined;          // Undefined during initial load
  isLoading: boolean;
  error: ApiError | undefined;
  mutate: () => Promise<void>;        // Manual revalidation
}
```

**Features**:
- Automatic caching and revalidation
- Revalidates on window focus / network reconnect
- Optimistic updates when mutations occur

**Usage**:
```tsx
import { useGoals } from '@/components/goals';

function MyComponent() {
  const { goals, isLoading, error } = useGoals('active');

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.detail}</div>;
  return <div>{goals?.length} goals</div>;
}
```

---

#### `useGoal(id)`
Fetches a single goal by ID (SWR-based).

**Parameters**:
- `id: string` (UUID)

**Returns** (`UseGoalResult`):
```typescript
{
  goal: Goal | null | undefined;      // Undefined during load, null if not found
  isLoading: boolean;
  error: ApiError | undefined;
  mutate: () => Promise<void>;
}
```

**Usage**:
```tsx
import { useGoal } from '@/components/goals';

function GoalDetail({ id }: { id: string }) {
  const { goal, isLoading, error } = useGoal(id);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.detail}</div>;
  if (!goal) return <div>Goal not found</div>;
  return <div>{goal.title}</div>;
}
```

---

#### `useGoalMutations()`
Provides mutation functions with optimistic updates.

**Returns** (`UseGoalMutationsResult`):
```typescript
{
  createGoal: (input: GoalCreateInput) => Promise<Goal>;
  updateGoal: (id: string, input: GoalUpdateInput) => Promise<Goal>;
  deleteGoal: (id: string) => Promise<void>;
  isMutating: boolean;                // True if any mutation in progress
}
```

**Features**:
- Optimistic UI updates (instant feedback)
- Automatic SWR cache invalidation
- Rollback on error
- Loading state tracking

**Usage**:
```tsx
import { useGoalMutations } from '@/components/goals';

function CreateGoalButton() {
  const { createGoal, isMutating } = useGoalMutations();

  const handleCreate = async () => {
    try {
      const goal = await createGoal({ title: 'New Goal' });
      console.log('Created:', goal);
    } catch (error) {
      console.error('Failed:', error);
    }
  };

  return <button onClick={handleCreate} disabled={isMutating}>Create</button>;
}
```

---

## Data Types

### Core Types (from `goals.d.ts`)

```typescript
// Domain entity
interface Goal {
  id: string;
  title: string;
  isDone: boolean;
  dateCreated: string;  // ISO 8601
  dateUpdated: string;  // ISO 8601
}

// Create input
interface GoalCreateInput {
  title: string;  // 1-255 chars, non-empty
}

// Update input
interface GoalUpdateInput {
  title?: string;   // 1-255 chars, optional
  isDone?: boolean; // Optional
}

// Filter status
type GoalFilterStatus = 'all' | 'active' | 'done';

// API error
interface ApiError {
  detail: string;
  type?: string;
  status?: number;
}
```

---

## API Client

### Internal Implementation (Not Public)
The module includes an internal `GoalsApi` implementation (`frontend/src/lib/api/goals.ts`) that handles HTTP requests to the backend. **This is not exposed as part of the public surface**—consumers should use hooks instead.

**Base URL**: `process.env.NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000`)

**Endpoints Mapping**:
- `listGoals(status)` → `GET /api/goals?status={status}`
- `getGoal(id)` → `GET /api/goals/{id}`
- `createGoal(input)` → `POST /api/goals`
- `updateGoal(id, input)` → `PATCH /api/goals/{id}`
- `deleteGoal(id)` → `DELETE /api/goals/{id}`

---

## Dependencies

This module depends on:
- **`backend.goals`**: Consumes REST API (OpenAPI contract)

**Allowed Imports from Dependencies**:
- None (only HTTP requests, no direct imports)

---

## Module Boundaries

### Allowed Directories
- `frontend/src/components/goals/**`
- `frontend/src/lib/api/goals.ts`
- `frontend/src/types/goal.ts`
- `frontend/src/app/**/goals/**` (if needed for page-specific logic)

### Internal Implementation (Not Public)
- API client class
- SWR configuration
- Internal utility functions

**Do not import internal implementation details from other modules.**

---

## Usage from Other Modules

### Import Hint
```typescript
// Components
import { GoalList, GoalForm, GoalItem } from '@/components/goals';

// Hooks
import { useGoals, useGoal, useGoalMutations } from '@/components/goals';

// Types (if needed)
import type { Goal, GoalCreateInput, GoalUpdateInput } from '@/components/goals';
```

### Example: Integrating into a Page
```tsx
// app/goals/page.tsx
'use client';

import { useState } from 'react';
import { GoalList, GoalForm, useGoalMutations } from '@/components/goals';

export default function GoalsPage() {
  const [filter, setFilter] = useState<'all' | 'active' | 'done'>('all');
  const { createGoal } = useGoalMutations();

  return (
    <div>
      <h1>My Goals</h1>
      <GoalForm onSave={(goal) => console.log('Created:', goal)} onCancel={() => {}} />
      <select value={filter} onChange={(e) => setFilter(e.target.value as any)}>
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="done">Done</option>
      </select>
      <GoalList filter={filter} />
    </div>
  );
}
```

---

## Styling

### Tailwind CSS
Components use Tailwind CSS v4 for styling. No CSS-in-JS or styled-components.

**Conventions**:
- Use Radix UI primitives for accessible components (dialogs, labels, etc.)
- Use `clsx` and `tailwind-merge` for conditional class names
- Follow existing design system (shadcn/ui patterns)

**Customization**:
All components accept a `className` prop for custom styling.

---

## Error Handling

### Backend Unavailable (FR-022-FR-025)
When backend is unavailable:
1. Display error banner: "Cannot connect to server. Please check your connection."
2. Disable all action buttons (Create, Edit, Delete, Toggle)
3. Show cached goals (if any) with stale indicator
4. Auto-retry on reconnect (SWR's `onReconnect`)

### Validation Errors (422)
Display error messages from API response:
- "Title cannot be empty or whitespace-only"
- "Title cannot exceed 255 characters"

### Not Found (404)
- `useGoal(id)` returns `goal: null` (not an error state)
- `deleteGoal(id)` silently succeeds (idempotent)

---

## Performance

- **SWR Caching**: Reduces redundant API calls
- **Optimistic Updates**: Instant UI feedback (no waiting for server)
- **Debouncing**: Filter changes debounced by 300ms
- **Bundle Size**: SWR adds ~15KB gzipped

---

## Testing Strategy

### Component Tests (Future)
- Vitest + React Testing Library
- Test user interactions (click, type, submit)
- Mock SWR hooks for isolated component testing

### Integration Tests (Future)
- E2E tests with Playwright
- Test full user flows (create → edit → toggle → delete)

---

## Versioning

**Current Version**: 0.1.0

**SemVer Policy**:
- **MAJOR**: Breaking changes to component props or hook return types
- **MINOR**: New components, hooks, or optional props
- **PATCH**: Bug fixes, styling updates, documentation

**Next Planned Version**: 0.2.0 (may add drag-and-drop reordering)

---

## Changelog

### 0.1.0 (2025-10-04)
- Initial release: `GoalList`, `GoalForm`, `GoalItem` components
- Hooks: `useGoals`, `useGoal`, `useGoalMutations`
- SWR-based state management with optimistic updates
- Tailwind CSS styling with Radix UI primitives
