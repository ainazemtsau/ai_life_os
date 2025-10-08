# Public Surface — frontend.design
Version: 0.1.0

## Purpose
Reusable UI components/tokens for all features.

## Public surface (imports)
- Components: `Button`, `Dialog`, `Input`, `Label`, `Card`, `Badge`, `DataTable`
- Utility: `cn`

## Usage
```ts
import { Button, DataTable } from '@/features/design';

const columns = [
  { id: "name", header: "Name" },
  { id: "status", header: "Status" },
];

<DataTable data={rows} columns={columns} />;
```

Rules

Import only from '@/features/design' (no deep imports).
