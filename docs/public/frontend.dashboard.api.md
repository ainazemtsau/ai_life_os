# Public API — frontend.dashboard
Version: 0.1.0

## Overview
Dashboard page module providing the main entry point UI for the application. Displays a welcoming dashboard with greeting, application information, and navigation to other features.

## Exports

### Components
- **`DashboardPage`** - Main dashboard page component that renders:
  - Greeting header ("Welcome to AI Life OS")
  - Welcome card with application purpose explanation
  - Available and upcoming features list
  - Quick actions card with navigation to Goals page

### Types
- **`DashboardPageProps`** - Props for DashboardPage component
  - `className?: string` - Optional styling customization

## Dependencies
- `frontend.design` - UI components (Card, Button, etc.)
- Next.js Link for navigation

## Types
Contract: frontend/src/contracts/dashboard.d.ts

## Usage
```ts
// Import the public surface
import * as dashboard from '@/features/dashboard'

// Use the component
<dashboard.DashboardPage />

// With custom styling
<dashboard.DashboardPage className="custom-wrapper" />
```

## Implementation Notes
- Uses namespace import pattern for design system (`import * as design from '@/features/design'`)
- Implements dark theme-compatible styling via design system
- Navigation to "/goals" via Next.js Link component
- Fully responsive layout with Tailwind CSS utilities

## Versioning
- 0.1.0 — Initial release
  - DashboardPage component
  - Greeting and welcome message
  - Navigation to Goals page
  - Dark theme support
