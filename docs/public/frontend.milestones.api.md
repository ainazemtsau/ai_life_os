# Public API — frontend.milestones
Version: 0.2.0

## Overview
Milestones UI module. Provides list page, CRUD forms, Goal selector, and API client hooks.

This module enables users to manage milestones associated with goals. It includes UI components for displaying, creating, editing and deleting milestones, along with hooks for interacting with the backend API.

## Exports
- `MilestonesList` - Component to display a list of milestones in a table format
- `MilestoneForm` - Component to create or edit a milestone with fields for title, goal selection, due date, status, demo criterion, and blocking status
- `useMilestones` - Hook to fetch list of milestones, with optional goal filtering
- `useCreateMilestone` - Hook to create a new milestone
- `useUpdateMilestone` - Hook to update an existing milestone
- `useDeleteMilestone` - Hook to delete a milestone
- `Milestone` - Type definition for the Milestone entity

## Types
Contract: frontend/src/contracts/milestones.d.ts

The Milestone type contains the following properties:
- `id`: string - Unique identifier for the milestone (UUID)
- `title`: string - Title of the milestone
- `goal_id`: string - Reference to the associated goal
- `due`: string (optional) - Due date in RFC 3339 format
- `status`: 'todo' | 'doing' | 'done' | 'blocked' - Current status of the milestone
- `demo_criterion`: string - Description of what constitutes completion
- `blocking`: boolean - Whether this milestone blocks other items
- `created_at`: string - Creation timestamp in RFC 3339 format
- `updated_at`: string - Last update timestamp in RFC 3339 format

## Usage
```ts
// public surface import
import * as milestones from '@/features/milestones'

// Example: Using the MilestonesList component
<MilestonesList 
  onMilestoneEdit={handleEdit} 
  onMilestoneDelete={handleDelete} 
/>

// Example: Using the MilestoneForm component
<MilestoneForm 
  onSubmit={handleSubmit} 
  onCancel={handleCancel} 
  goals={availableGoals} 
/>

// Example: Using the hooks
const { milestones, loading, error } = milestones.useMilestones();
const { mutate: createMilestone } = milestones.useCreateMilestone();
const { mutate: updateMilestone } = milestones.useUpdateMilestone();
const { mutate: deleteMilestone } = milestones.useDeleteMilestone();
```

## Dependencies
- `frontend.design` - Used for UI components and styling
- `backend.milestones` - Provides the API contract for milestone operations
- `backend.goals` - Provides goal data for the goal selector

## Versioning
- 0.1.0 — Initial stub
- 0.2.0 — Added Milestones UI components and hooks
