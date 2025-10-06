# Public Surface — frontend.goals
Version: 0.1.0

## Purpose
UI components & hooks for goals. Consumes `backend.goals` via OpenAPI-generated types/SDK.

## Public surface (imports)
- Components: `GoalList`, `GoalForm`, `GoalItem`
- Hooks: `useGoals(filter?: 'all'|'active'|'done')`, `useGoal(id: string)`, `useGoalMutations()`

## Usage
```ts
import { GoalList } from '@/features/goals';
import { useGoals } from '@/features/goals';
Notes
Data types/SDK are generated from backend OpenAPI (outside /plan).