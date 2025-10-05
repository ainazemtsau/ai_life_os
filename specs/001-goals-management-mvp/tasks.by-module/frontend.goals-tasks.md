# Module Tasks: frontend.goals for Feature 001-goals-management-mvp

**Inputs**:
- Global constitution: `.specify/memory/constitution.md`
- Module constitution: None (uses global only)
- Global tasks: `specs/001-goals-management-mvp/tasks.md`
- Manifest: `.specify/memory/public/frontend.goals.api.md`
- Contract: `frontend/src/contracts/goals.d.ts`

**Dependencies** (opaque, use manifest/contract only):
- **frontend.design** - Design system components (Button, Dialog, Input, Label, Card, Badge)
- **backend.goals** - REST API (HTTP only, OpenAPI spec)

**Scope**:
- Allowed directories: `frontend/src/features/goals/**`, `frontend/src/contracts/goals.d.ts`
- Work ONLY inside allowed paths

---

## Execution Flow

This module provides Goals Management UI (GoalList, GoalForm, GoalItem components) and SWR-based hooks (useGoals, useGoal, useGoalMutations). It consumes backend.goals REST API and uses frontend.design components.

**TDD Order**: API client → Hooks (with mocks) → Components (with hook mocks) → Integration → Docs sync

---

## Phase A: Setup

### MT001 Create module directory structure

**Description**: Create frontend.goals module skeleton within allowed directories.

**Files**:
- `frontend/src/features/goals/` (directory)
- `frontend/src/features/goals/lib/` (API client)
- `frontend/src/features/goals/hooks/` (SWR hooks)
- `frontend/src/features/goals/components/` (React components)
- `frontend/src/features/goals/index.ts` (barrel export)

**Dependencies**: None (can run first)

**Detailed Steps**:
1. Create directory structure:
   ```bash
   mkdir -p frontend/src/features/goals/lib
   mkdir -p frontend/src/features/goals/hooks
   mkdir -p frontend/src/features/goals/components
   ```

2. Create barrel export file `frontend/src/features/goals/index.ts`:
   ```typescript
   // Re-export hooks
   export * from './hooks/useGoals';
   export * from './hooks/useGoal';
   export * from './hooks/useGoalMutations';

   // Re-export components
   export * from './components/GoalList';
   export * from './components/GoalForm';
   export * from './components/GoalItem';
   ```

**Acceptance Criteria**:
- [ ] Directory `frontend/src/features/goals/lib/` exists
- [ ] Directory `frontend/src/features/goals/hooks/` exists
- [ ] Directory `frontend/src/features/goals/components/` exists
- [ ] File `frontend/src/features/goals/index.ts` exists with barrel exports

**Validation**:
```bash
ls -la frontend/src/features/goals/{lib,hooks,components}
cat frontend/src/features/goals/index.ts
```

---

### MT002 Install SWR dependency

**Description**: Add SWR library for data fetching and caching.

**File**: `frontend/package.json` (via pnpm)

**Dependencies**: None (parallel with MT001)

**Detailed Steps**:
1. Install SWR:
   ```bash
   cd frontend && pnpm add swr
   ```

2. Verify installation:
   ```bash
   pnpm list | grep swr
   ```

**Acceptance Criteria**:
- [ ] `swr` package installed
- [ ] `pnpm.lock` updated
- [ ] Version is compatible with React 19

**Validation**:
```bash
cat frontend/package.json | grep -A2 '"swr"'
```

---

## Phase B: API Client Implementation

### MT010 Implement Goals API client

**Description**: Create HTTP client for backend.goals REST API (based on OpenAPI contract).

**File**: `frontend/src/features/goals/lib/api.ts`

**Dependencies**: MT001 (directory structure), backend.goals OpenAPI contract (opaque)

**Detailed Steps**:
1. Create `frontend/src/features/goals/lib/api.ts`:
   ```typescript
   import type {
     Goal,
     GoalCreateInput,
     GoalUpdateInput,
     GoalFilterStatus,
     ApiError,
     GoalsApi,
   } from '@/contracts/goals';

   /**
    * Goals API client implementation.
    * Communicates with backend.goals REST API at /api/goals.
    */
   class GoalsApiClient implements GoalsApi {
     private baseUrl: string;

     constructor() {
       this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
     }

     async listGoals(status?: GoalFilterStatus): Promise<Goal[]> {
       const url = new URL('/api/goals', this.baseUrl);
       if (status && status !== 'all') {
         url.searchParams.set('status', status);
       }

       const response = await fetch(url.toString());
       if (!response.ok) {
         throw await this.handleError(response);
       }

       const data = await response.json();
       return this.mapGoalsFromApi(data.goals);
     }

     async getGoal(id: string): Promise<Goal | null> {
       const url = new URL(`/api/goals/${id}`, this.baseUrl);
       const response = await fetch(url.toString());

       if (response.status === 404) {
         return null;
       }

       if (!response.ok) {
         throw await this.handleError(response);
       }

       const data = await response.json();
       return this.mapGoalFromApi(data);
     }

     async createGoal(input: GoalCreateInput): Promise<Goal> {
       const url = new URL('/api/goals', this.baseUrl);
       const response = await fetch(url.toString(), {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ title: input.title }),
       });

       if (!response.ok) {
         throw await this.handleError(response);
       }

       const data = await response.json();
       return this.mapGoalFromApi(data);
     }

     async updateGoal(id: string, input: GoalUpdateInput): Promise<Goal> {
       const url = new URL(`/api/goals/${id}`, this.baseUrl);
       const body: any = {};
       if (input.title !== undefined) body.title = input.title;
       if (input.isDone !== undefined) body.is_done = input.isDone;

       const response = await fetch(url.toString(), {
         method: 'PATCH',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(body),
       });

       if (!response.ok) {
         throw await this.handleError(response);
       }

       const data = await response.json();
       return this.mapGoalFromApi(data);
     }

     async deleteGoal(id: string): Promise<boolean> {
       const url = new URL(`/api/goals/${id}`, this.baseUrl);
       const response = await fetch(url.toString(), {
         method: 'DELETE',
       });

       if (response.status === 404) {
         return false;
       }

       if (!response.ok && response.status !== 204) {
         throw await this.handleError(response);
       }

       return true;
     }

     /**
      * Map backend snake_case to frontend camelCase
      */
     private mapGoalFromApi(data: any): Goal {
       return {
         id: data.id,
         title: data.title,
         isDone: data.is_done,
         dateCreated: data.date_created,
         dateUpdated: data.date_updated,
       };
     }

     private mapGoalsFromApi(data: any[]): Goal[] {
       return data.map((item) => this.mapGoalFromApi(item));
     }

     private async handleError(response: Response): Promise<ApiError> {
       let detail = 'An unexpected error occurred';
       let type = 'unknown_error';

       try {
         const data = await response.json();
         detail = data.detail || detail;
         type = data.type || type;
       } catch {
         // Fallback if response is not JSON
       }

       return {
         detail,
         type,
         status: response.status,
       };
     }
   }

   export const goalsApi = new GoalsApiClient();
   ```

2. Verify TypeScript contract alignment:
   ```bash
   cd frontend && pnpm typecheck
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/lib/api.ts` exists
- [ ] Implements GoalsApi interface from contract
- [ ] All 5 HTTP methods implemented (GET list, GET single, POST, PATCH, DELETE)
- [ ] Maps backend snake_case (is_done, date_created) to frontend camelCase (isDone, dateCreated)
- [ ] Uses NEXT_PUBLIC_API_URL from environment
- [ ] Error handling with ApiError type
- [ ] Returns null for 404 in getGoal
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/lib/api.ts
cd frontend && pnpm typecheck
```

---

## Phase C: SWR Hooks Implementation

### MT020 [P] Implement useGoals hook

**Description**: Create SWR hook for fetching goals list with filtering and caching.

**File**: `frontend/src/features/goals/hooks/useGoals.ts`

**Dependencies**: MT010 (API client)

**Detailed Steps**:
1. Create `frontend/src/features/goals/hooks/useGoals.ts`:
   ```typescript
   'use client';

   import useSWR from 'swr';
   import type { GoalFilterStatus, UseGoalsResult } from '@/contracts/goals';
   import { goalsApi } from '../lib/api';

   /**
    * SWR hook for fetching goals list with automatic caching and revalidation.
    *
    * @param filter - Filter by completion status ('all', 'active', 'done')
    * @returns Goals list, loading state, error, and mutate function
    */
   export function useGoals(filter: GoalFilterStatus = 'all'): UseGoalsResult {
     const { data, error, isLoading, mutate } = useSWR(
       `/api/goals?status=${filter}`,
       () => goalsApi.listGoals(filter),
       {
         revalidateOnFocus: true,
         revalidateOnReconnect: true,
       }
     );

     return {
       goals: data,
       isLoading,
       error,
       mutate: async () => {
         await mutate();
       },
     };
   }
   ```

2. Export from hooks index:
   ```bash
   echo "export { useGoals } from './useGoals';" >> frontend/src/features/goals/hooks/index.ts
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/hooks/useGoals.ts` exists
- [ ] Returns UseGoalsResult type from contract
- [ ] Uses SWR with cache key including filter
- [ ] Revalidates on focus and reconnect
- [ ] Defaults to 'all' filter
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/hooks/useGoals.ts
cd frontend && pnpm typecheck
```

---

### MT021 [P] Implement useGoal hook

**Description**: Create SWR hook for fetching a single goal by ID.

**File**: `frontend/src/features/goals/hooks/useGoal.ts`

**Dependencies**: MT010 (API client)

**Detailed Steps**:
1. Create `frontend/src/features/goals/hooks/useGoal.ts`:
   ```typescript
   'use client';

   import useSWR from 'swr';
   import type { UseGoalResult } from '@/contracts/goals';
   import { goalsApi } from '../lib/api';

   /**
    * SWR hook for fetching a single goal by ID.
    *
    * @param id - Goal UUID
    * @returns Goal object (null if not found), loading state, error, and mutate function
    */
   export function useGoal(id: string): UseGoalResult {
     const { data, error, isLoading, mutate } = useSWR(
       id ? `/api/goals/${id}` : null,
       () => goalsApi.getGoal(id),
       {
         revalidateOnFocus: true,
       }
     );

     return {
       goal: data,
       isLoading,
       error,
       mutate: async () => {
         await mutate();
       },
     };
   }
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/hooks/useGoal.ts` exists
- [ ] Returns UseGoalResult type from contract
- [ ] Uses SWR with cache key `/api/goals/{id}`
- [ ] Returns null if goal not found (404)
- [ ] Skips fetch if id is falsy (conditional fetching)
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/hooks/useGoal.ts
cd frontend && pnpm typecheck
```

---

### MT022 Implement useGoalMutations hook

**Description**: Create hook for goal mutations (create, update, delete) with optimistic updates.

**File**: `frontend/src/features/goals/hooks/useGoalMutations.ts`

**Dependencies**: MT020, MT021 (needs SWR cache invalidation)

**Detailed Steps**:
1. Create `frontend/src/features/goals/hooks/useGoalMutations.ts`:
   ```typescript
   'use client';

   import { useState } from 'react';
   import { mutate } from 'swr';
   import type {
     GoalCreateInput,
     GoalUpdateInput,
     UseGoalMutationsResult,
   } from '@/contracts/goals';
   import { goalsApi } from '../lib/api';

   /**
    * Hook for goal mutations with optimistic updates and SWR cache invalidation.
    */
   export function useGoalMutations(): UseGoalMutationsResult {
     const [isMutating, setIsMutating] = useState(false);

     const createGoal = async (input: GoalCreateInput) => {
       setIsMutating(true);
       try {
         const goal = await goalsApi.createGoal(input);
         // Invalidate all goals lists
         await mutate(
           (key) => typeof key === 'string' && key.startsWith('/api/goals?'),
           undefined,
           { revalidate: true }
         );
         return goal;
       } finally {
         setIsMutating(false);
       }
     };

     const updateGoal = async (id: string, input: GoalUpdateInput) => {
       setIsMutating(true);
       try {
         const goal = await goalsApi.updateGoal(id, input);
         // Invalidate single goal and all lists
         await mutate(`/api/goals/${id}`, goal, { revalidate: false });
         await mutate(
           (key) => typeof key === 'string' && key.startsWith('/api/goals?'),
           undefined,
           { revalidate: true }
         );
         return goal;
       } finally {
         setIsMutating(false);
       }
     };

     const deleteGoal = async (id: string) => {
       setIsMutating(true);
       try {
         await goalsApi.deleteGoal(id);
         // Invalidate single goal and all lists
         await mutate(`/api/goals/${id}`, null, { revalidate: false });
         await mutate(
           (key) => typeof key === 'string' && key.startsWith('/api/goals?'),
           undefined,
           { revalidate: true }
         );
       } finally {
         setIsMutating(false);
       }
     };

     return {
       createGoal,
       updateGoal,
       deleteGoal,
       isMutating,
     };
   }
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/hooks/useGoalMutations.ts` exists
- [ ] Returns UseGoalMutationsResult type from contract
- [ ] createGoal invalidates all list caches
- [ ] updateGoal invalidates single goal + all lists
- [ ] deleteGoal invalidates single goal + all lists
- [ ] isMutating tracks mutation state
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/hooks/useGoalMutations.ts
cd frontend && pnpm typecheck
```

---

## Phase D: React Components Implementation

### MT030 Implement GoalItem component

**Description**: Create single goal row component with inline actions (toggle, edit, delete).

**File**: `frontend/src/features/goals/components/GoalItem.tsx`

**Dependencies**: MT010 (API client), frontend.design components (opaque, use contract only)

**Detailed Steps**:
1. Create `frontend/src/features/goals/components/GoalItem.tsx`:
   ```typescript
   'use client';

   import type { GoalItemProps } from '@/contracts/goals';
   import { Button, Badge } from '@/features/design';
   import { cn } from '@/features/design';

   /**
    * Single goal item with inline actions.
    * Displays title, status badge, and action buttons (toggle, edit, delete).
    */
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
           'flex items-center justify-between gap-4 p-4 rounded-lg border bg-card',
           goal.isDone && 'opacity-60',
           className
         )}
       >
         <div className="flex items-center gap-3 flex-1 min-w-0">
           <input
             type="checkbox"
             checked={goal.isDone}
             onChange={(e) => onToggle(goal.id, e.target.checked)}
             className="h-4 w-4 rounded border-gray-300"
             aria-label={`Mark "${goal.title}" as ${goal.isDone ? 'active' : 'done'}`}
           />
           <div className="flex-1 min-w-0">
             <p
               className={cn(
                 'text-sm font-medium truncate',
                 goal.isDone && 'line-through text-muted-foreground'
               )}
             >
               {goal.title}
             </p>
             <p className="text-xs text-muted-foreground">
               Updated {new Date(goal.dateUpdated).toLocaleDateString()}
             </p>
           </div>
           <Badge variant={goal.isDone ? 'secondary' : 'default'}>
             {goal.isDone ? 'Done' : 'Active'}
           </Badge>
         </div>

         <div className="flex items-center gap-2">
           <Button
             variant="ghost"
             size="sm"
             onClick={() => onEdit(goal)}
             aria-label={`Edit goal "${goal.title}"`}
           >
             Edit
           </Button>
           <Button
             variant="ghost"
             size="sm"
             onClick={() => onDelete(goal.id)}
             aria-label={`Delete goal "${goal.title}"`}
           >
             Delete
           </Button>
         </div>
       </div>
     );
   }
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/components/GoalItem.tsx` exists
- [ ] Accepts GoalItemProps from contract
- [ ] Uses Button and Badge from frontend.design
- [ ] Checkbox for toggle with aria-label
- [ ] Displays title (line-through if done)
- [ ] Displays date updated
- [ ] Edit and Delete buttons with aria-labels
- [ ] Opacity reduced for completed goals
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/components/GoalItem.tsx
cd frontend && pnpm typecheck
```

---

### MT031 Implement GoalForm component

**Description**: Create form component for creating/editing goals with validation.

**File**: `frontend/src/features/goals/components/GoalForm.tsx`

**Dependencies**: MT010 (API client), frontend.design components (opaque)

**Detailed Steps**:
1. Create `frontend/src/features/goals/components/GoalForm.tsx`:
   ```typescript
   'use client';

   import { useState } from 'react';
   import type { GoalFormProps } from '@/contracts/goals';
   import { Button, Input, Label } from '@/features/design';
   import { cn } from '@/features/design';

   /**
    * Form for creating or editing a goal.
    * Validates title length (1-255 characters).
    */
   export function GoalForm({ goal, onSave, onCancel, className }: GoalFormProps) {
     const [title, setTitle] = useState(goal?.title || '');
     const [error, setError] = useState<string | null>(null);

     const handleSubmit = (e: React.FormEvent) => {
       e.preventDefault();

       const trimmedTitle = title.trim();
       if (!trimmedTitle) {
         setError('Title cannot be empty');
         return;
       }
       if (trimmedTitle.length > 255) {
         setError('Title cannot exceed 255 characters');
         return;
       }

       setError(null);
       // Simulate save (actual save handled by parent via useGoalMutations)
       onSave({ ...goal!, title: trimmedTitle });
     };

     return (
       <form onSubmit={handleSubmit} className={cn('space-y-4', className)}>
         <div className="space-y-2">
           <Label htmlFor="goal-title">
             {goal ? 'Edit Goal' : 'New Goal'}
           </Label>
           <Input
             id="goal-title"
             type="text"
             value={title}
             onChange={(e) => setTitle(e.target.value)}
             placeholder="Enter goal title..."
             error={!!error}
             maxLength={255}
             aria-describedby={error ? 'goal-title-error' : undefined}
           />
           {error && (
             <p id="goal-title-error" className="text-sm text-destructive">
               {error}
             </p>
           )}
         </div>

         <div className="flex justify-end gap-2">
           <Button type="button" variant="ghost" onClick={onCancel}>
             Cancel
           </Button>
           <Button type="submit">
             {goal ? 'Save Changes' : 'Create Goal'}
           </Button>
         </div>
       </form>
     );
   }
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/components/GoalForm.tsx` exists
- [ ] Accepts GoalFormProps from contract
- [ ] Uses Input, Label, Button from frontend.design
- [ ] Validates title (1-255 chars, non-empty)
- [ ] Shows error state in Input component
- [ ] Submit button text changes based on mode (create/edit)
- [ ] Calls onSave with updated goal
- [ ] Calls onCancel when cancelled
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/components/GoalForm.tsx
cd frontend && pnpm typecheck
```

---

### MT032 Implement GoalList component

**Description**: Create list component with filtering and integration with useGoals hook.

**File**: `frontend/src/features/goals/components/GoalList.tsx`

**Dependencies**: MT020 (useGoals hook), MT022 (useGoalMutations hook), MT030 (GoalItem component)

**Detailed Steps**:
1. Create `frontend/src/features/goals/components/GoalList.tsx`:
   ```typescript
   'use client';

   import { useState } from 'react';
   import type { GoalListProps, Goal } from '@/contracts/goals';
   import { useGoals } from '../hooks/useGoals';
   import { useGoalMutations } from '../hooks/useGoalMutations';
   import { GoalItem } from './GoalItem';
   import { GoalForm } from './GoalForm';
   import { Button, Dialog, DialogContent, DialogHeader, DialogTitle } from '@/features/design';
   import { cn } from '@/features/design';

   /**
    * List of goals with filtering, inline actions, and create/edit dialogs.
    */
   export function GoalList({ filter = 'all', onGoalClick, className }: GoalListProps) {
     const { goals, isLoading, error } = useGoals(filter);
     const { updateGoal, deleteGoal } = useGoalMutations();
     const [editingGoal, setEditingGoal] = useState<Goal | null>(null);

     const handleToggle = async (id: string, isDone: boolean) => {
       await updateGoal(id, { isDone });
     };

     const handleEdit = (goal: Goal) => {
       setEditingGoal(goal);
     };

     const handleSaveEdit = async (goal: Goal) => {
       await updateGoal(goal.id, { title: goal.title });
       setEditingGoal(null);
     };

     const handleDelete = async (id: string) => {
       if (confirm('Are you sure you want to delete this goal?')) {
         await deleteGoal(id);
       }
     };

     if (isLoading) {
       return <div className="text-center py-8 text-muted-foreground">Loading goals...</div>;
     }

     if (error) {
       return (
         <div className="text-center py-8 text-destructive">
           Error loading goals: {error.detail}
         </div>
       );
     }

     if (!goals || goals.length === 0) {
       return (
         <div className="text-center py-8 text-muted-foreground">
           No {filter !== 'all' ? filter : ''} goals found. Create one to get started!
         </div>
       );
     }

     return (
       <>
         <div className={cn('space-y-2', className)}>
           {goals.map((goal) => (
             <GoalItem
               key={goal.id}
               goal={goal}
               onToggle={handleToggle}
               onEdit={handleEdit}
               onDelete={handleDelete}
             />
           ))}
         </div>

         <Dialog open={!!editingGoal} onOpenChange={(open) => !open && setEditingGoal(null)}>
           <DialogContent>
             <DialogHeader>
               <DialogTitle>Edit Goal</DialogTitle>
             </DialogHeader>
             {editingGoal && (
               <GoalForm
                 goal={editingGoal}
                 onSave={handleSaveEdit}
                 onCancel={() => setEditingGoal(null)}
               />
             )}
           </DialogContent>
         </Dialog>
       </>
     );
   }
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/goals/components/GoalList.tsx` exists
- [ ] Accepts GoalListProps from contract
- [ ] Uses useGoals and useGoalMutations hooks
- [ ] Displays loading state
- [ ] Displays error state
- [ ] Displays empty state with filter-aware message
- [ ] Maps goals to GoalItem components
- [ ] Opens Dialog for editing
- [ ] Confirms before delete
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/goals/components/GoalList.tsx
cd frontend && pnpm typecheck
```

---

## Phase E: Next.js Integration

### MT040 Wire Goals page to Next.js App Router

**Description**: Create Next.js page component at /goals route using App Router.

**File**: `frontend/src/app/goals/page.tsx`

**Dependencies**: MT032 (GoalList component), MT022 (useGoalMutations hook), MT031 (GoalForm component)

**Detailed Steps**:
1. Create `frontend/src/app/goals/page.tsx`:
   ```typescript
   'use client';

   import { useState } from 'react';
   import { GoalList, GoalForm, useGoalMutations } from '@/features/goals';
   import { Card, CardHeader, CardTitle, CardContent, Button } from '@/features/design';

   export default function GoalsPage() {
     const [filter, setFilter] = useState<'all' | 'active' | 'done'>('all');
     const [showCreateForm, setShowCreateForm] = useState(false);
     const { createGoal } = useGoalMutations();

     const handleCreate = async (input: { title: string }) => {
       await createGoal({ title: input.title });
       setShowCreateForm(false);
     };

     return (
       <div className="container mx-auto py-8 max-w-4xl">
         <Card>
           <CardHeader>
             <div className="flex items-center justify-between">
               <CardTitle>My Goals</CardTitle>
               <Button onClick={() => setShowCreateForm(!showCreateForm)}>
                 {showCreateForm ? 'Cancel' : 'New Goal'}
               </Button>
             </div>
           </CardHeader>

           <CardContent className="space-y-6">
             {showCreateForm && (
               <GoalForm
                 onSave={handleCreate}
                 onCancel={() => setShowCreateForm(false)}
               />
             )}

             <div className="flex gap-2">
               <Button
                 variant={filter === 'all' ? 'default' : 'outline'}
                 size="sm"
                 onClick={() => setFilter('all')}
               >
                 All
               </Button>
               <Button
                 variant={filter === 'active' ? 'default' : 'outline'}
                 size="sm"
                 onClick={() => setFilter('active')}
               >
                 Active
               </Button>
               <Button
                 variant={filter === 'done' ? 'default' : 'outline'}
                 size="sm"
                 onClick={() => setFilter('done')}
               >
                 Done
               </Button>
             </div>

             <GoalList filter={filter} />
           </CardContent>
         </Card>
       </div>
     );
   }
   ```

2. Update TypeScript path alias (if needed):
   ```bash
   # Verify @/features/* alias in tsconfig.json
   grep -A5 '"paths"' frontend/tsconfig.json
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/app/goals/page.tsx` exists
- [ ] Uses GoalList, GoalForm components from @/features/goals
- [ ] Uses Card, Button from @/features/design
- [ ] Filter buttons (All, Active, Done)
- [ ] Toggle create form visibility
- [ ] Calls createGoal mutation
- [ ] Client component ('use client')
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/app/goals/page.tsx
cd frontend && pnpm typecheck
```

---

## Phase F: Docs Sync & Validation

### MT050 Update TypeScript contract with actual implementations

**Description**: Verify TypeScript contract matches implemented component/hook signatures.

**File**: `frontend/src/contracts/goals.d.ts`

**Dependencies**: MT040 (all implementations complete)

**Detailed Steps**:
1. Review `frontend/src/contracts/goals.d.ts` against implementations
2. Ensure all exported types match actual component props and hook return types
3. Add any missing type exports discovered during implementation

**Note**: Contract was pre-populated during `/plan`. Only update if implementation revealed discrepancies.

**Acceptance Criteria**:
- [ ] All component prop types match implementations
- [ ] All hook return types match implementations
- [ ] GoalsApi interface matches api.ts implementation
- [ ] No type mismatches
- [ ] TypeScript check passes

**Validation**:
```bash
cd frontend && pnpm typecheck
diff <(grep -E "^export (interface|const|function|type)" frontend/src/features/goals/index.ts | sort) \
     <(grep -E "^export (interface|const|function|type)" frontend/src/contracts/goals.d.ts | sort)
```

---

### MT051 Update manifest with component/hook documentation

**Description**: Update frontend.goals manifest with usage examples and implementation notes.

**File**: `.specify/memory/public/frontend.goals.api.md`

**Dependencies**: MT050 (contract verified)

**Detailed Steps**:
1. Review manifest at `.specify/memory/public/frontend.goals.api.md`
2. Add usage examples for components and hooks
3. Document SWR caching behavior
4. Add error handling notes
5. Document optimistic updates

**Note**: Manifest was pre-populated during `/plan`. Enhance with actual usage patterns.

**Acceptance Criteria**:
- [ ] All 3 components documented (GoalList, GoalForm, GoalItem)
- [ ] All 3 hooks documented (useGoals, useGoal, useGoalMutations)
- [ ] Usage examples provided
- [ ] SWR caching behavior documented
- [ ] Optimistic updates documented
- [ ] Dependencies listed (frontend.design, backend.goals, SWR)
- [ ] Import hint verified

**Validation**:
```bash
cat .specify/memory/public/frontend.goals.api.md
python .specify/scripts/manifest_lint.py
```

---

### MT052 Bump module SemVer and validate registry

**Description**: Update module version in registry (0.1.0 → 0.1.0 for initial release) and run validators.

**File**: `.specify/memory/public/registry.yaml`

**Dependencies**: MT051 (manifest updated)

**Detailed Steps**:
1. Review module version in registry (already at 0.1.0 for initial MVP)
2. Run registry validator:
   ```bash
   python .specify/scripts/registry_validate.py
   ```
3. Run manifest linter:
   ```bash
   python .specify/scripts/manifest_lint.py
   ```

**Note**: For initial MVP release, version remains 0.1.0. Future changes will increment per SemVer policy.

**Acceptance Criteria**:
- [ ] Registry version is 0.1.0 (initial release)
- [ ] `registry_validate.py` passes
- [ ] `manifest_lint.py` passes
- [ ] Contract path verified: `frontend/src/contracts/goals.d.ts`
- [ ] Manifest path verified: `.specify/memory/public/frontend.goals.api.md`
- [ ] Dependencies verified: frontend.design, backend.goals

**Validation**:
```bash
python .specify/scripts/registry_validate.py
python .specify/scripts/manifest_lint.py
cat .specify/memory/public/registry.yaml | grep -A15 "frontend.goals"
```

---

### MT053 Accessibility audit (WCAG 2.1 AA)

**Description**: Verify WCAG 2.1 AA compliance for all components.

**Dependencies**: MT040 (all components implemented)

**Detailed Steps**:
1. Verify keyboard navigation:
   - Tab through all interactive elements
   - Enter/Space to activate buttons
   - Escape to close dialogs
2. Verify ARIA attributes:
   - Checkboxes have aria-label
   - Buttons have aria-label for icon-only
   - Error messages use aria-describedby
   - Dialog has proper aria-labelledby
3. Verify color contrast (via browser DevTools or axe extension)
4. Verify focus indicators visible

**Acceptance Criteria**:
- [ ] All interactive elements keyboard accessible
- [ ] All form controls have labels (explicit or aria-label)
- [ ] Error messages associated with inputs (aria-describedby)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus indicators visible for all interactive elements
- [ ] Dialog trap focus and close on Escape
- [ ] Screen reader friendly (semantic HTML, ARIA)

**Validation**:
```bash
# Manual testing required
# Use browser DevTools Accessibility tab
# Use axe DevTools browser extension
# Test with keyboard only (no mouse)
```

---

## Dependencies

```
MT001 (setup) + MT002 (SWR) → MT010 (API client)
                               ↓
                            MT020 (useGoals) + MT021 (useGoal)
                               ↓
                            MT022 (useGoalMutations)
                               ↓
                            MT030 (GoalItem) + MT031 (GoalForm)
                               ↓
                            MT032 (GoalList)
                               ↓
                            MT040 (Next.js page)
                               ↓
                            MT050 (contract) → MT051 (manifest) → MT052 (validators)
                               ↓
                            MT053 (accessibility)
```

## Parallel Execution

**Can run in parallel**:
- MT001 + MT002 (setup tasks, no dependencies)
- MT020 + MT021 (both hooks after MT010)
- MT030 + MT031 (both components use same dependencies)

**Sequential**:
- MT010 must complete before MT020/MT021 (hooks need API client)
- MT022 after MT020/MT021 (mutations need cache invalidation)
- MT032 after MT022, MT030, MT031 (uses all hooks and components)
- MT040 after MT032 (page uses GoalList)
- MT050-MT053 run sequentially (docs sync + validation)

**Example parallel launch**:
```bash
# After MT010 completes:
Task MT020 (useGoals) & Task MT021 (useGoal) & wait

# After MT022 completes:
Task MT030 (GoalItem) & Task MT031 (GoalForm) & wait
```

---

## Validation Checklist

After completing all frontend.goals tasks:
- [ ] All 3 hooks implemented (useGoals, useGoal, useGoalMutations)
- [ ] All 3 components implemented (GoalList, GoalForm, GoalItem)
- [ ] Goals API client working (5 HTTP methods)
- [ ] SWR caching and revalidation functional
- [ ] Optimistic updates working
- [ ] Next.js page at /goals route functional
- [ ] All files within `allowed_dirs` (frontend/src/features/goals/**)
- [ ] TypeScript check passes: `cd frontend && pnpm typecheck`
- [ ] Barrel export functional: `import * from '@/features/goals'`
- [ ] Contract matches implementation
- [ ] Manifest updated with usage docs
- [ ] Registry validators pass
- [ ] Uses frontend.design components correctly (Button, Dialog, Input, Label, Card, Badge)
- [ ] Consumes backend.goals REST API correctly (snake_case to camelCase mapping)
- [ ] WCAG 2.1 AA compliance verified
- [ ] Ready for end-to-end testing

---

## Notes

- This module **depends on** frontend.design (components) and backend.goals (REST API)
- All dependencies are opaque: only use manifests and contracts
- SWR provides automatic caching, revalidation, and optimistic updates
- API client maps backend snake_case to frontend camelCase
- Components follow React best practices (controlled inputs, event handlers)
- Accessibility built-in (keyboard navigation, ARIA, semantic HTML)
- Error handling with user-friendly messages
- Confirmation dialog before destructive actions (delete)

**Commit after each task**: `feat(frontend.goals): <task description> [MT###]`

<!-- FANOUT:BEGIN -->
## Global Items (source)

*Do not edit this block manually; run `/fanout-tasks` to refresh.*

- [ ] T003 @module(frontend.goals) @prio(P1) Add SWR dependency via pnpm
- [ ] T030 @module(frontend.goals) @prio(P1) Implement Goals API client (HTTP methods)
- [ ] T031 @module(frontend.goals) @prio(P1) Implement useGoals hook (SWR-based list)
- [ ] T032 @module(frontend.goals) @prio(P1) Implement useGoal hook (SWR-based single)
- [ ] T033 @module(frontend.goals) @prio(P1) Implement useGoalMutations hook (create/update/delete with optimistic updates)
- [ ] T034 @module(frontend.goals) @prio(P1) Implement GoalList component with filtering
- [ ] T035 @module(frontend.goals) @prio(P1) Implement GoalForm component (create/edit modes)
- [ ] T036 @module(frontend.goals) @prio(P1) Implement GoalItem component with inline actions
- [ ] T051 @module(frontend.goals) @prio(P1) Wire Goals page to Next.js App Router
- [ ] T061 @module(frontend.goals) @prio(P2) Update manifest with final component/hook signatures
- [ ] T065 @module(frontend.goals) @prio(P3) Accessibility audit: WCAG 2.1 AA compliance
<!-- FANOUT:END -->
