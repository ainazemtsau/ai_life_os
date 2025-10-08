# TypeScript Strict Mode Development Guide

**Project**: AI Life OS
**Created**: 2025-10-07
**Purpose**: Prevent common TypeScript errors when implementing frontend modules with strict compiler options

---

## Overview

This project uses **strict TypeScript configuration** with these critical settings:

```json
{
  "verbatimModuleSyntax": true,
  "noPropertyAccessFromIndexSignature": true,
  "exactOptionalPropertyTypes": true,
  "noUncheckedIndexedAccess": true
}
```

These settings improve type safety but require careful coding patterns. This guide shows correct implementations.

---

## 1. Type-Only Imports (`verbatimModuleSyntax: true`)

### ❌ Wrong
```typescript
import { Milestone } from "@/features/milestones/types";
import { Goal, Project } from "./types";
```

### ✅ Correct
```typescript
import type { Milestone } from "@/features/milestones/types";
import type { Goal, Project } from "./types";
```

**Rule**: If you only use a name as a **type** (not as a value), use `import type`.

**Examples**:
- Type annotations: `const x: Milestone` → use `import type`
- Component props: `interface Props { goal: Goal }` → use `import type`
- Values/functions: `import { useMilestones } from "./hooks"` → regular import

---

## 2. Index Signature Access (`noPropertyAccessFromIndexSignature: true`)

### ❌ Wrong
```typescript
const errors: Record<string, string> = {};
errors.title = "Required";
if (errors.title) { /* ... */ }
```

### ✅ Correct
```typescript
const errors: Record<string, string> = {};
errors["title"] = "Required";
if (errors["title"]) { /* ... */ }
```

**Rule**: For `Record<string, T>` or index signatures, use **bracket notation** `obj["key"]` instead of dot notation `obj.key`.

**Note**: Concrete types (not Records) can still use dot notation:
```typescript
interface User { name: string }
const user: User = { name: "Alice" };
console.log(user.name); // ✅ OK - concrete type, not index signature
```

---

## 3. Exact Optional Properties (`exactOptionalPropertyTypes: true`)

### ❌ Wrong
```typescript
// Contract
interface HookReturn {
  error?: string;  // means: property might not exist
}

// Implementation
function useData(): HookReturn {
  const [error, setError] = useState<string | undefined>(undefined);
  return { error };  // ❌ error is ALWAYS present (just undefined)
}
```

### ✅ Correct - Option A (Conditional Return)
```typescript
function useData(): HookReturn {
  const [error, setError] = useState<string | undefined>(undefined);
  return error ? { data, error } : { data };  // ✅ property conditionally included
}
```

### ✅ Correct - Option B (Change Contract)
```typescript
// If error is always present, update contract:
interface HookReturn {
  error: string | undefined;  // property always exists
}
```

**Rule**: `error?: string` means the property **might not exist** in the object. It's different from `error: string | undefined` (property always exists, value might be undefined).

---

## 4. Vitest (Not Jest) for Tests

### ❌ Wrong (Jest)
```typescript
import { MockedProvider } from "@apollo/client/testing";

jest.mock("./hooks", () => ({
  useData: jest.fn()
}));

test("it works", () => {
  (useData as jest.Mock).mockReturnValue(...);
});
```

### ✅ Correct (Vitest)
```typescript
import { describe, test, expect, vi, beforeEach } from "vitest";

vi.mock("./hooks", () => ({
  useData: vi.fn()
}));

test("it works", () => {
  vi.mocked(useData).mockReturnValue(...);
});
```

**Rule**: This project uses **Vitest**, not Jest:
- Import test globals from `"vitest"`
- Use `vi.fn()`, `vi.mock()`, `vi.mocked()`
- No `MockedProvider` (not using Apollo GraphQL)

---

## 5. Optional Property Access (`noUncheckedIndexedAccess: true`)

### ❌ Wrong
```typescript
const formData = { due?: string };
const formatted = formData.due.split("T")[0];  // ❌ due might be undefined
```

### ✅ Correct
```typescript
const formatted = formData.due ? formData.due.split("T")[0] : "";  // ✅ check first
// or
const formatted = formData.due?.split("T")[0] ?? "";  // ✅ optional chaining
```

**Rule**: Check optional properties before accessing them.

---

## 6. Floating Promises in useEffect

### ❌ Wrong
```typescript
useEffect(() => {
  fetchData();  // ❌ floating promise
}, []);
```

### ✅ Correct
```typescript
const fetchData = useCallback(async () => {
  try {
    const data = await api.getData();
    setData(data);
  } catch (err) {
    setError(err.message);
  }
}, []);

useEffect(() => {
  fetchData().catch((err) => {
    console.error("Error:", err);
  });
}, [fetchData]);
```

**Rule**:
- Wrap async functions in `useCallback` with proper dependencies
- Add `.catch()` handler to promises in useEffect
- Include the callback in useEffect dependencies

---

## 7. Enum/Union Types with `as const`

### ❌ Wrong (in tests/mocks)
```typescript
const mockProject = {
  status: "todo",  // ❌ type is 'string', not '"todo"'
};
```

### ✅ Correct
```typescript
const mockProject = {
  status: "todo" as const,  // ✅ type is '"todo"'
};
```

**Rule**: For strict union types (`"todo" | "doing" | "done"`), use `as const` in test data to ensure literal types.

---

## 8. Import Organization

### ✅ Correct Order
```typescript
// 1. React
import React from "react";

// 2. External libraries
import { render, screen } from "@testing-library/react";
import { describe, test, vi } from "vitest";

// 3. Type imports (from contracts/external)
import type { Milestone } from "@/contracts/milestones.d";

// 4. Internal imports (same feature)
import { useMilestones } from "./hooks";
import { MilestonesList } from "./MilestonesList";

// 5. Local types
import type { LocalType } from "./types";
```

**Rule**: ESLint enforces import order. Run `pnpm lint:fix` to auto-fix.

---

## 9. Hook Return Type Patterns

### Pattern: Data Fetching Hook
```typescript
interface UseDataReturn {
  data: Data[];
  loading: boolean;
  error?: string;  // optional - might not be present
  refetch: () => void;
}

export function useData(): UseDataReturn {
  const [data, setData] = useState<Data[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | undefined>(undefined);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(undefined);
      const result = await api.getData();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData().catch(console.error);
  }, [fetchData]);

  const refetch = useCallback(() => {
    fetchData().catch(console.error);
  }, [fetchData]);

  // Return error conditionally (exactOptionalPropertyTypes)
  return error
    ? { data, loading, error, refetch }
    : { data, loading, refetch };
}
```

### Pattern: Mutation Hook
```typescript
interface UseMutationReturn {
  mutate: (item: Item) => Promise<void>;
  loading: boolean;
  error?: string;
}

export function useCreateItem(): UseMutationReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const mutate = async (item: Item) => {
    try {
      setLoading(true);
      setError(undefined);
      await api.createItem(item);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  };

  return error
    ? { mutate, loading, error }
    : { mutate, loading };
}
```

---

## 10. Form Validation Patterns

### Pattern: Form with Record Errors
```typescript
export const MyForm: React.FC<Props> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({ title: "", description: "" });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors: Record<string, string> = {};
    if (!formData.title) {
      newErrors["title"] = "Required";  // ✅ bracket notation
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="title"
        value={formData.title}
        onChange={handleChange}
      />
      {errors["title"] && <span>{errors["title"]}</span>}  {/* ✅ bracket notation */}
    </form>
  );
};
```

---

## Checklist for New Frontend Modules

Before running `/module-verify`:

- [ ] All type imports use `import type { ... }`
- [ ] Record/index signature access uses bracket notation `obj["key"]`
- [ ] Optional properties in contracts match implementation (conditional return or `T | undefined`)
- [ ] Test files use Vitest (`vi.mock`, `vi.fn`, `vi.mocked`)
- [ ] Test mock data uses `as const` for union types
- [ ] No `MockedProvider` or other Apollo/GraphQL testing utilities
- [ ] useEffect with async calls have `.catch()` handlers
- [ ] Async functions in hooks wrapped in `useCallback`
- [ ] Optional property access has guards (`?.` or explicit checks)
- [ ] Imports organized correctly (run `pnpm lint:fix`)
- [ ] UI rendering behavior covered via higher-level tests (skip unit tests that only assert static DOM structure or labels)

---

## Quick Reference

| Setting | Requires | Example |
|---------|----------|---------|
| `verbatimModuleSyntax` | `import type` for types | `import type { User } from "./types"` |
| `noPropertyAccessFromIndexSignature` | Bracket notation for Records | `errors["field"]` not `errors.field` |
| `exactOptionalPropertyTypes` | Conditional property inclusion | `error ? { ...data, error } : { ...data }` |
| `noUncheckedIndexedAccess` | Check before access | `arr[0]?.prop ?? defaultValue` |

---

## Common Errors and Fixes

### Error: `TS2305: Module has no exported member 'X'`
**Cause**: Importing type as value
**Fix**: Change to `import type { X }`

### Error: `TS4111: Property 'x' comes from an index signature`
**Cause**: Dot notation on Record type
**Fix**: Use `obj["x"]` instead of `obj.x`

### Error: `TS2375: Type is not assignable with 'exactOptionalPropertyTypes: true'`
**Cause**: Property with `| undefined` doesn't match optional property `?`
**Fix**: Return conditionally: `error ? { ...data, error } : { ...data }`

### Error: `TS18048: 'x' is possibly 'undefined'`
**Cause**: Accessing optional property without check
**Fix**: Add guard: `x ? x.method() : defaultValue`

### Error: `@typescript-eslint/no-floating-promises`
**Cause**: Promise not handled in useEffect
**Fix**: Add `.catch()`: `fetchData().catch(console.error)`

---

## Resources

- [TypeScript Handbook: Modules](https://www.typescriptlang.org/docs/handbook/modules.html#import-type)
- [Vitest API](https://vitest.dev/api/)
- [React Hooks Reference](https://react.dev/reference/react/hooks)
