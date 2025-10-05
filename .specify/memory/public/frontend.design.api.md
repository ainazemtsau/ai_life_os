# Public API — frontend.design
Version: 0.1.0

## Overview
Foundational design system providing reusable UI components, design tokens, and accessibility patterns for all frontend features. Built on Radix UI primitives with Tailwind CSS 4 styling. Ensures consistent user experience across the application.

## Exports
### Components (based on shadcn/ui patterns)
- `Button` - Primary action component with variants (default, destructive, outline, ghost)
- `Dialog` - Modal dialog with accessibility (keyboard navigation, focus trap)
- `Input` - Text input with validation states
- `Label` - Form label with proper association
- `Card` - Container component for grouped content
- `Badge` - Status indicator (active, done, etc.)

### Utilities
- `cn` - Class name merger (clsx + tailwind-merge)

## Types
Contract: `frontend/src/contracts/design.d.ts`

**Key types:**
- `ButtonProps` - Extends React.ButtonHTMLAttributes with variant/size props
- `DialogProps` - Modal configuration and content props
- `InputProps` - Extends React.InputHTMLAttributes with validation state
- `LabelProps` - Form label props
- `CardProps` - Container styling props
- `BadgeProps` - Status badge variant props

## Usage
```ts
import { Button, Dialog, Input, Label } from '@/features/design';

function MyForm() {
  return (
    <div>
      <Label htmlFor="title">Title</Label>
      <Input id="title" placeholder="Enter title" />
      <Button variant="default">Submit</Button>
    </div>
  );
}
```

## Stability
- exports: **experimental** (v0.1.0 - component API may evolve)
- types: **experimental** (props may refine based on usage patterns)

## Dependencies
- No module dependencies (foundational layer)
- External: React 19, Radix UI, Tailwind CSS 4, class-variance-authority

## Versioning
- **0.1.0** - Initial MVP release with core components
- SemVer policy: MAJOR for breaking component API changes, MINOR for new components, PATCH for styling fixes

## Notes
- All components are server-component compatible (Next.js 15)
- Accessibility built-in via Radix UI (ARIA attributes, keyboard navigation)
- Tailwind CSS 4 for styling (no CSS-in-JS)
- Dark mode ready (will be implemented in future version)
- Components follow atomic design principles (atoms → molecules → organisms)
