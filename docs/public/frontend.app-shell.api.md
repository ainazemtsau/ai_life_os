# Public API — frontend.app-shell
Version: 0.1.0

## Overview
App shell and routing module for AI Life OS. Provides the root application layout with dark theme configuration and route components that wire feature modules into Next.js App Router. This module owns the `frontend/src/app/**` directory (Next.js routing glue).

## Exports

### Components

#### `AppLayout`
Root application layout component that provides consistent theme and structure across all pages.

**Props**: `AppLayoutProps`
- `children: React.ReactNode` - Child components to render within the layout
- `className?: string` - Optional className for additional styling

**Features**:
- Applies dark theme by default
- Provides consistent background and text colors
- Wraps all application content

#### `DashboardRoute`
Dashboard route component that wraps `DashboardPage` from `frontend.dashboard` module.

**Props**: None

**Usage**: Use in Next.js App Router page components (`app/page.tsx`)

#### `GoalsRoute`
Goals route component that wraps goals page content from `frontend.goals` module.

**Props**: None

**Usage**: Use in Next.js App Router page components (`app/goals/page.tsx`)

## Types
Contract: `frontend/src/contracts/app-shell.d.ts`

### `AppLayoutProps`
```typescript
interface AppLayoutProps {
  children: React.ReactNode;
  className?: string;
}
```

## Usage

### Basic Import Pattern
```typescript
// Always use namespace imports for module boundaries
import * as appShell from '@/features/app-shell'
```

### Root Layout (app/layout.tsx)
```typescript
import * as appShell from '@/features/app-shell'

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body>
        <appShell.AppLayout>{children}</appShell.AppLayout>
      </body>
    </html>
  )
}
```

### Route Pages
```typescript
// app/page.tsx
import * as appShell from '@/features/app-shell'

export default function Page() {
  return <appShell.DashboardRoute />
}

// app/goals/page.tsx
import * as appShell from '@/features/app-shell'

export default function GoalsPage() {
  return <appShell.GoalsRoute />
}
```

## Dependencies
- **frontend.dashboard** - Provides `DashboardPage` component
- **frontend.goals** - Provides goals page components
- **frontend.design** - Provides utility functions (`cn`)

## Notes
- Dark theme is applied by default; no theme switcher in this version
- This module owns `frontend/src/app/**` for Next.js routing configuration
- Route components are minimal wrappers that delegate to feature modules
- All framework-specific (Next.js) code is isolated in this module

## Versioning
- 0.1.0 — Initial implementation with AppLayout, DashboardRoute, and GoalsRoute; dark theme by default [public-api]
