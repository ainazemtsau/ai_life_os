# Module Tasks: frontend.design for Feature 001-goals-management-mvp

**Inputs**:
- Global constitution: `.specify/memory/constitution.md`
- Module constitution: None (uses global only)
- Global tasks: `specs/001-goals-management-mvp/tasks.md`
- Manifest: `.specify/memory/public/frontend.design.api.md`
- Contract: `frontend/src/contracts/design.d.ts`

**Scope**:
- Allowed directories: `frontend/src/features/design/**`, `frontend/src/contracts/design.d.ts`
- No dependencies (foundational module)
- Work ONLY inside allowed paths

---

## Execution Flow

This module provides the foundational design system (Button, Dialog, Input, Label, Card, Badge, cn utility). All components follow shadcn/ui patterns with Radix UI primitives and Tailwind CSS 4 styling.

**TDD Order**: Component contract verification → Implementation → Visual/accessibility tests → Docs sync

---

## Phase A: Setup

### MT001 Create module directory structure

**Description**: Create frontend.design module skeleton within allowed directories.

**Files**:
- `frontend/src/features/design/` (directory)
- `frontend/src/features/design/components/` (directory)
- `frontend/src/features/design/utils/` (directory)
- `frontend/src/features/design/index.ts` (barrel export)

**Dependencies**: None (can run first)

**Detailed Steps**:
1. Create directory structure:
   ```bash
   mkdir -p frontend/src/features/design/components
   mkdir -p frontend/src/features/design/utils
   ```

2. Create barrel export file `frontend/src/features/design/index.ts`:
   ```typescript
   // Re-export all components and utilities
   export * from './components/button';
   export * from './components/dialog';
   export * from './components/input';
   export * from './components/label';
   export * from './components/card';
   export * from './components/badge';
   export * from './utils/cn';
   ```

**Acceptance Criteria**:
- [ ] Directory `frontend/src/features/design/components/` exists
- [ ] Directory `frontend/src/features/design/utils/` exists
- [ ] File `frontend/src/features/design/index.ts` exists with barrel exports

**Validation**:
```bash
ls -la frontend/src/features/design/components
ls -la frontend/src/features/design/utils
cat frontend/src/features/design/index.ts
```

---

### MT002 [P] Install design system dependencies

**Description**: Add required npm packages for design system (Radix UI, Tailwind utilities).

**File**: `frontend/package.json` (via pnpm)

**Dependencies**: None (parallel with MT001)

**Detailed Steps**:
1. Install Radix UI primitives:
   ```bash
   cd frontend && pnpm add @radix-ui/react-dialog @radix-ui/react-label
   ```

2. Install utility libraries:
   ```bash
   pnpm add class-variance-authority clsx tailwind-merge
   ```

3. Verify installation:
   ```bash
   pnpm list | grep -E "(radix|clsx|tailwind-merge|class-variance-authority)"
   ```

**Acceptance Criteria**:
- [ ] `@radix-ui/react-dialog` installed
- [ ] `@radix-ui/react-label` installed
- [ ] `class-variance-authority` installed
- [ ] `clsx` installed
- [ ] `tailwind-merge` installed
- [ ] `pnpm.lock` updated

**Validation**:
```bash
cat frontend/package.json | grep -A5 '"dependencies"'
```

---

## Phase B: Utility Implementation (Foundation)

### MT010 Implement cn utility function

**Description**: Create class name merger utility (clsx + tailwind-merge).

**File**: `frontend/src/features/design/utils/cn.ts`

**Dependencies**: MT002 (needs clsx and tailwind-merge installed)

**Detailed Steps**:
1. Create `frontend/src/features/design/utils/cn.ts`:
   ```typescript
   import { clsx, type ClassValue } from 'clsx';
   import { twMerge } from 'tailwind-merge';

   /**
    * Merges class names with Tailwind CSS conflict resolution.
    * Combines clsx for conditional classes and tailwind-merge for deduplication.
    *
    * @param inputs - Class names (strings, objects, arrays, booleans, undefined, null)
    * @returns Merged class name string
    *
    * @example
    * cn('px-2 py-1', 'px-4') // => 'py-1 px-4' (px-2 overridden)
    * cn('text-red-500', isError && 'text-blue-500') // => conditional
    */
   export function cn(...inputs: ClassValue[]): string {
     return twMerge(clsx(inputs));
   }
   ```

2. Verify TypeScript contract alignment:
   ```bash
   cd frontend && pnpm typecheck
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/utils/cn.ts` exists
- [ ] Function signature matches contract: `cn(...inputs: (string | undefined | null | boolean)[]): string`
- [ ] Uses clsx for conditional logic
- [ ] Uses tailwind-merge for Tailwind conflict resolution
- [ ] JSDoc comment included
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/utils/cn.ts
cd frontend && pnpm typecheck
```

---

## Phase C: Component Implementation

### MT020 [P] Implement Button component

**Description**: Create Button component with variants (default, destructive, outline, ghost, link) and sizes.

**File**: `frontend/src/features/design/components/button.tsx`

**Dependencies**: MT010 (cn utility)

**Detailed Steps**:
1. Create `frontend/src/features/design/components/button.tsx`:
   ```typescript
   import * as React from 'react';
   import { Slot } from '@radix-ui/react-slot';
   import { cva, type VariantProps } from 'class-variance-authority';
   import { cn } from '../utils/cn';

   const buttonVariants = cva(
     'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
     {
       variants: {
         variant: {
           default: 'bg-primary text-primary-foreground hover:bg-primary/90',
           destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
           outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
           ghost: 'hover:bg-accent hover:text-accent-foreground',
           link: 'text-primary underline-offset-4 hover:underline',
         },
         size: {
           default: 'h-10 px-4 py-2',
           sm: 'h-9 rounded-md px-3',
           lg: 'h-11 rounded-md px-8',
           icon: 'h-10 w-10',
         },
       },
       defaultVariants: {
         variant: 'default',
         size: 'default',
       },
     }
   );

   export interface ButtonProps
     extends React.ButtonHTMLAttributes<HTMLButtonElement>,
       VariantProps<typeof buttonVariants> {
     asChild?: boolean;
   }

   const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
     ({ className, variant, size, asChild = false, ...props }, ref) => {
       const Comp = asChild ? Slot : 'button';
       return (
         <Comp
           className={cn(buttonVariants({ variant, size, className }))}
           ref={ref}
           {...props}
         />
       );
     }
   );
   Button.displayName = 'Button';

   export { Button, buttonVariants };
   ```

2. Install missing dependency:
   ```bash
   cd frontend && pnpm add @radix-ui/react-slot
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/components/button.tsx` exists
- [ ] ButtonProps matches contract (variant, size, asChild)
- [ ] All 5 variants implemented: default, destructive, outline, ghost, link
- [ ] All 4 sizes implemented: default, sm, lg, icon
- [ ] Uses cn utility for class merging
- [ ] Supports asChild prop (Radix Slot pattern)
- [ ] Forward ref for accessibility
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/components/button.tsx
cd frontend && pnpm typecheck
```

---

### MT021 [P] Implement Dialog component

**Description**: Create accessible Dialog (modal) component using Radix UI primitives.

**File**: `frontend/src/features/design/components/dialog.tsx`

**Dependencies**: MT010 (cn utility)

**Detailed Steps**:
1. Create `frontend/src/features/design/components/dialog.tsx`:
   ```typescript
   'use client';

   import * as React from 'react';
   import * as DialogPrimitive from '@radix-ui/react-dialog';
   import { X } from 'lucide-react';
   import { cn } from '../utils/cn';

   const Dialog = DialogPrimitive.Root;
   const DialogTrigger = DialogPrimitive.Trigger;
   const DialogPortal = DialogPrimitive.Portal;
   const DialogClose = DialogPrimitive.Close;

   const DialogOverlay = React.forwardRef<
     React.ElementRef<typeof DialogPrimitive.Overlay>,
     React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
   >(({ className, ...props }, ref) => (
     <DialogPrimitive.Overlay
       ref={ref}
       className={cn(
         'fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
         className
       )}
       {...props}
     />
   ));
   DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

   const DialogContent = React.forwardRef<
     React.ElementRef<typeof DialogPrimitive.Content>,
     React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
   >(({ className, children, ...props }, ref) => (
     <DialogPortal>
       <DialogOverlay />
       <DialogPrimitive.Content
         ref={ref}
         className={cn(
           'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg',
           className
         )}
         {...props}
       >
         {children}
         <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
           <X className="h-4 w-4" />
           <span className="sr-only">Close</span>
         </DialogPrimitive.Close>
       </DialogPrimitive.Content>
     </DialogPortal>
   ));
   DialogContent.displayName = DialogPrimitive.Content.displayName;

   const DialogHeader = ({
     className,
     ...props
   }: React.HTMLAttributes<HTMLDivElement>) => (
     <div
       className={cn('flex flex-col space-y-1.5 text-center sm:text-left', className)}
       {...props}
     />
   );
   DialogHeader.displayName = 'DialogHeader';

   const DialogTitle = React.forwardRef<
     React.ElementRef<typeof DialogPrimitive.Title>,
     React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
   >(({ className, ...props }, ref) => (
     <DialogPrimitive.Title
       ref={ref}
       className={cn('text-lg font-semibold leading-none tracking-tight', className)}
       {...props}
     />
   ));
   DialogTitle.displayName = DialogPrimitive.Title.displayName;

   const DialogDescription = React.forwardRef<
     React.ElementRef<typeof DialogPrimitive.Description>,
     React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
   >(({ className, ...props }, ref) => (
     <DialogPrimitive.Description
       ref={ref}
       className={cn('text-sm text-muted-foreground', className)}
       {...props}
     />
   ));
   DialogDescription.displayName = DialogPrimitive.Description.displayName;

   export {
     Dialog,
     DialogPortal,
     DialogOverlay,
     DialogClose,
     DialogTrigger,
     DialogContent,
     DialogHeader,
     DialogTitle,
     DialogDescription,
   };
   ```

2. Install icon library:
   ```bash
   cd frontend && pnpm add lucide-react
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/components/dialog.tsx` exists
- [ ] All Dialog subcomponents exported: Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription
- [ ] Uses Radix UI Dialog primitives
- [ ] Keyboard navigation support (Escape to close)
- [ ] Focus trap implemented
- [ ] Close button with X icon
- [ ] Proper ARIA attributes (via Radix)
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/components/dialog.tsx
cd frontend && pnpm typecheck
```

---

### MT022 [P] Implement Input component

**Description**: Create text Input component with error state styling.

**File**: `frontend/src/features/design/components/input.tsx`

**Dependencies**: MT010 (cn utility)

**Detailed Steps**:
1. Create `frontend/src/features/design/components/input.tsx`:
   ```typescript
   import * as React from 'react';
   import { cn } from '../utils/cn';

   export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
     error?: boolean;
   }

   const Input = React.forwardRef<HTMLInputElement, InputProps>(
     ({ className, type, error, ...props }, ref) => {
       return (
         <input
           type={type}
           className={cn(
             'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
             error && 'border-destructive focus-visible:ring-destructive',
             className
           )}
           ref={ref}
           {...props}
         />
       );
     }
   );
   Input.displayName = 'Input';

   export { Input };
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/components/input.tsx` exists
- [ ] InputProps matches contract (error?: boolean)
- [ ] Error state applies destructive styling
- [ ] Forward ref for form integration
- [ ] Supports all standard input attributes
- [ ] Tailwind focus-visible ring
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/components/input.tsx
cd frontend && pnpm typecheck
```

---

### MT023 [P] Implement Label component

**Description**: Create accessible Label component using Radix UI primitive.

**File**: `frontend/src/features/design/components/label.tsx`

**Dependencies**: MT010 (cn utility)

**Detailed Steps**:
1. Create `frontend/src/features/design/components/label.tsx`:
   ```typescript
   'use client';

   import * as React from 'react';
   import * as LabelPrimitive from '@radix-ui/react-label';
   import { cva, type VariantProps } from 'class-variance-authority';
   import { cn } from '../utils/cn';

   const labelVariants = cva(
     'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'
   );

   const Label = React.forwardRef<
     React.ElementRef<typeof LabelPrimitive.Root>,
     React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root> &
       VariantProps<typeof labelVariants>
   >(({ className, ...props }, ref) => (
     <LabelPrimitive.Root
       ref={ref}
       className={cn(labelVariants(), className)}
       {...props}
     />
   ));
   Label.displayName = LabelPrimitive.Root.displayName;

   export { Label };
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/components/label.tsx` exists
- [ ] Uses Radix Label primitive
- [ ] Proper htmlFor association (via Radix)
- [ ] Peer-disabled styling support
- [ ] Forward ref
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/components/label.tsx
cd frontend && pnpm typecheck
```

---

### MT024 [P] Implement Card components

**Description**: Create Card component family (Card, CardHeader, CardTitle, CardDescription, CardContent).

**File**: `frontend/src/features/design/components/card.tsx`

**Dependencies**: MT010 (cn utility)

**Detailed Steps**:
1. Create `frontend/src/features/design/components/card.tsx`:
   ```typescript
   import * as React from 'react';
   import { cn } from '../utils/cn';

   const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
     ({ className, ...props }, ref) => (
       <div
         ref={ref}
         className={cn('rounded-lg border bg-card text-card-foreground shadow-sm', className)}
         {...props}
       />
     )
   );
   Card.displayName = 'Card';

   const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
     ({ className, ...props }, ref) => (
       <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
     )
   );
   CardHeader.displayName = 'CardHeader';

   const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
     ({ className, ...props }, ref) => (
       <h3
         ref={ref}
         className={cn('text-2xl font-semibold leading-none tracking-tight', className)}
         {...props}
       />
     )
   );
   CardTitle.displayName = 'CardTitle';

   const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
     ({ className, ...props }, ref) => (
       <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
     )
   );
   CardDescription.displayName = 'CardDescription';

   const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
     ({ className, ...props }, ref) => (
       <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
     )
   );
   CardContent.displayName = 'CardContent';

   export { Card, CardHeader, CardTitle, CardDescription, CardContent };
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/components/card.tsx` exists
- [ ] All 5 Card components exported
- [ ] Card container with border and shadow
- [ ] CardHeader with proper spacing
- [ ] CardTitle as semantic h3
- [ ] CardDescription with muted color
- [ ] CardContent with padding
- [ ] Forward refs on all components
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/components/card.tsx
cd frontend && pnpm typecheck
```

---

### MT025 [P] Implement Badge component

**Description**: Create Badge component with variants (default, secondary, destructive, outline).

**File**: `frontend/src/features/design/components/badge.tsx`

**Dependencies**: MT010 (cn utility)

**Detailed Steps**:
1. Create `frontend/src/features/design/components/badge.tsx`:
   ```typescript
   import * as React from 'react';
   import { cva, type VariantProps } from 'class-variance-authority';
   import { cn } from '../utils/cn';

   const badgeVariants = cva(
     'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
     {
       variants: {
         variant: {
           default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
           secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
           destructive: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
           outline: 'text-foreground',
         },
       },
       defaultVariants: {
         variant: 'default',
       },
     }
   );

   export interface BadgeProps
     extends React.HTMLAttributes<HTMLDivElement>,
       VariantProps<typeof badgeVariants> {}

   function Badge({ className, variant, ...props }: BadgeProps) {
     return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
   }

   export { Badge, badgeVariants };
   ```

**Acceptance Criteria**:
- [ ] File `frontend/src/features/design/components/badge.tsx` exists
- [ ] BadgeProps matches contract (variant: default | secondary | destructive | outline)
- [ ] All 4 variants implemented
- [ ] Rounded-full pill shape
- [ ] Focus ring for keyboard navigation
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/components/badge.tsx
cd frontend && pnpm typecheck
```

---

## Phase D: Integration & Export

### MT030 Update barrel export with all components

**Description**: Update main index.ts to re-export all implemented components and utilities.

**File**: `frontend/src/features/design/index.ts`

**Dependencies**: MT020-MT025 (all components)

**Detailed Steps**:
1. Update `frontend/src/features/design/index.ts`:
   ```typescript
   // Utilities
   export { cn } from './utils/cn';

   // Components
   export { Button, buttonVariants, type ButtonProps } from './components/button';
   export {
     Dialog,
     DialogPortal,
     DialogOverlay,
     DialogClose,
     DialogTrigger,
     DialogContent,
     DialogHeader,
     DialogTitle,
     DialogDescription,
     type DialogProps,
     type DialogTriggerProps,
     type DialogContentProps,
     type DialogHeaderProps,
     type DialogTitleProps,
     type DialogDescriptionProps,
   } from './components/dialog';
   export { Input, type InputProps } from './components/input';
   export { Label } from './components/label';
   export {
     Card,
     CardHeader,
     CardTitle,
     CardDescription,
     CardContent,
     type CardProps,
     type CardHeaderProps,
     type CardTitleProps,
     type CardDescriptionProps,
     type CardContentProps,
   } from './components/card';
   export { Badge, badgeVariants, type BadgeProps } from './components/badge';
   ```

2. Verify imports work:
   ```bash
   cd frontend && pnpm typecheck
   ```

**Acceptance Criteria**:
- [ ] All components re-exported
- [ ] All type definitions re-exported
- [ ] cn utility re-exported
- [ ] No circular dependencies
- [ ] Import hint works: `import * as design from '@/features/design'`
- [ ] TypeScript check passes

**Validation**:
```bash
cat frontend/src/features/design/index.ts
cd frontend && pnpm typecheck
```

---

## Phase E: Docs Sync & Validation

### MT040 Update TypeScript contract with actual implementations

**Description**: Verify TypeScript contract matches implemented component signatures.

**File**: `frontend/src/contracts/design.d.ts`

**Dependencies**: MT030 (all components implemented)

**Detailed Steps**:
1. Review `frontend/src/contracts/design.d.ts` against implementations
2. Ensure all exported types match actual component props
3. Add any missing type exports discovered during implementation

**Note**: Contract was pre-populated during `/plan`. Only update if implementation revealed discrepancies.

**Acceptance Criteria**:
- [ ] All component types match implementations
- [ ] ButtonProps includes variant, size, asChild
- [ ] Dialog subcomponents all defined
- [ ] InputProps includes error property
- [ ] Card subcomponents all defined
- [ ] BadgeProps includes variant
- [ ] cn utility signature correct
- [ ] No type mismatches

**Validation**:
```bash
cd frontend && pnpm typecheck
diff <(grep -E "^export (interface|const|function|type)" frontend/src/features/design/index.ts | sort) \
     <(grep -E "^export (interface|const|function|type)" frontend/src/contracts/design.d.ts | sort)
```

---

### MT041 Update manifest with component documentation

**Description**: Update frontend.design manifest with usage examples and implementation notes.

**File**: `.specify/memory/public/frontend.design.api.md`

**Dependencies**: MT030 (all components implemented)

**Detailed Steps**:
1. Review manifest at `.specify/memory/public/frontend.design.api.md`
2. Add usage examples for each component
3. Document accessibility features (ARIA, keyboard navigation)
4. Add installation/setup notes (Radix UI, Tailwind, lucide-react)

**Note**: Manifest was pre-populated during `/plan`. Enhance with actual usage patterns.

**Acceptance Criteria**:
- [ ] All 6 components documented
- [ ] cn utility documented
- [ ] Usage examples provided
- [ ] Accessibility notes included
- [ ] Dependencies listed (Radix UI, Tailwind, lucide-react)
- [ ] Import hint verified

**Validation**:
```bash
cat .specify/memory/public/frontend.design.api.md
python .specify/scripts/manifest_lint.py
```

---

### MT042 Bump module SemVer and validate registry

**Description**: Update module version in registry (0.1.0 → 0.1.0 for initial release) and run validators.

**File**: `.specify/memory/public/registry.yaml`

**Dependencies**: MT041 (manifest updated)

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
- [ ] Contract path verified: `frontend/src/contracts/design.d.ts`
- [ ] Manifest path verified: `.specify/memory/public/frontend.design.api.md`

**Validation**:
```bash
python .specify/scripts/registry_validate.py
python .specify/scripts/manifest_lint.py
cat .specify/memory/public/registry.yaml | grep -A10 "frontend.design"
```

---

## Dependencies

```
MT001 (setup) → MT010 (cn utility)
                  ↓
MT002 (deps) ──→ MT020–MT025 (components, parallel)
                  ↓
              MT030 (barrel export)
                  ↓
              MT040 (contract verification)
                  ↓
              MT041 (manifest update)
                  ↓
              MT042 (semver + validators)
```

## Parallel Execution

**Can run in parallel**:
- MT001 + MT002 (setup tasks, no dependencies)
- MT020–MT025 (all component implementations after MT010 completes)

**Sequential**:
- MT010 must complete before MT020-MT025 (components need cn utility)
- MT030 after all components (barrel export)
- MT040-MT042 run sequentially (docs sync)

**Example parallel launch**:
```bash
# After MT010 completes, launch all component tasks together:
Task MT020 (Button) &
Task MT021 (Dialog) &
Task MT022 (Input) &
Task MT023 (Label) &
Task MT024 (Card) &
Task MT025 (Badge) &
wait
```

---

## Validation Checklist

After completing all frontend.design tasks:
- [ ] All 6 components implemented (Button, Dialog, Input, Label, Card, Badge)
- [ ] cn utility working
- [ ] TypeScript check passes: `cd frontend && pnpm typecheck`
- [ ] Barrel export functional: `import * as design from '@/features/design'`
- [ ] Contract matches implementation
- [ ] Manifest updated with usage docs
- [ ] Registry validators pass
- [ ] No dependencies on other modules (foundational)
- [ ] Radix UI accessibility features working (keyboard nav, ARIA)
- [ ] Tailwind CSS 4 styling applied
- [ ] Ready for frontend.goals consumption

---

## Notes

- This is a **foundational module** with no dependencies
- All components follow shadcn/ui patterns for consistency
- Accessibility built-in via Radix UI primitives
- Components are server-compatible (Next.js 15 App Router)
- Tailwind CSS 4 used for styling (no CSS-in-JS)
- Class variance authority for variant management
- Forward refs for form integration and accessibility
- Dark mode styling ready (will activate when theme provider added)

**Commit after each task**: `feat(frontend.design): <task description> [MT###]`

<!-- FANOUT:BEGIN -->
## Global Items (source)

*Do not edit this block manually; run `/fanout-tasks` to refresh.*

- [ ] T020 @module(frontend.design) @prio(P1) Implement Button component with variants
- [ ] T021 @module(frontend.design) @prio(P1) Implement Dialog component (Radix UI wrapper)
- [ ] T022 @module(frontend.design) @prio(P1) Implement Input component with error state
- [ ] T023 @module(frontend.design) @prio(P1) Implement Label component
- [ ] T024 @module(frontend.design) @prio(P2) Implement Card components (Card, CardHeader, CardContent)
- [ ] T025 @module(frontend.design) @prio(P2) Implement Badge component with variants
- [ ] T026 @module(frontend.design) @prio(P1) Implement cn utility (clsx + tailwind-merge)
- [ ] T062 @module(frontend.design) @prio(P2) Update manifest with design system components
<!-- FANOUT:END -->
