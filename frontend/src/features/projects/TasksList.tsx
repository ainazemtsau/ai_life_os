import React from "react";

import { Button, DataTable, type DataTableColumn } from "@/features/design";
import type { Task } from "@/features/projects/types";

import { useTasks } from "./hooks";

const toTitleCase = (value: string): string =>
  value.length > 0 ? value.charAt(0).toUpperCase() + value.slice(1) : value;

const renderEnumCell = (value: unknown): React.ReactNode => {
  if (typeof value === "string" && value.length > 0) {
    return toTitleCase(value);
  }

  if (value === null || value === undefined) {
    return <span className="text-muted-foreground">—</span>;
  }

  if (typeof value === "number") {
    return value;
  }

  return String(value);
};

interface TasksListProps {
  onTaskEdit?: (task: Task) => void;
  onTaskDelete?: (task: Task) => void;
  filterByProject?: string;
}

export const TasksList: React.FC<TasksListProps> = ({
  onTaskEdit,
  onTaskDelete,
  filterByProject,
}) => {
  // Using the hook to get tasks data
  const { tasks, loading, error } = useTasks(filterByProject);

  const columns = React.useMemo<DataTableColumn<Task>[]>(
    () => [
      {
        id: "title",
        header: "Title",
        accessor: "title",
      },
      {
        id: "project",
        header: "Project",
        accessor: (task) => task.project_id,
      },
      {
        id: "status",
        header: "Status",
        cell: ({ row }) => (
          <span className={`status-${row.status}`}>{toTitleCase(row.status)}</span>
        ),
      },
      {
        id: "size",
        header: "Size",
        accessor: (task) => task.size,
        cell: ({ value }) => renderEnumCell(value),
      },
      {
        id: "energy",
        header: "Energy",
        accessor: (task) => task.energy,
        cell: ({ value }) => renderEnumCell(value),
      },
      {
        id: "continuity",
        header: "Continuity",
        accessor: (task) => task.continuity,
        cell: ({ value }) => renderEnumCell(value),
      },
      {
        id: "clarity",
        header: "Clarity",
        accessor: (task) => task.clarity,
        cell: ({ value }) => renderEnumCell(value),
      },
      {
        id: "risk",
        header: "Risk",
        accessor: (task) => task.risk,
        cell: ({ value }) => renderEnumCell(value),
      },
      {
        id: "dependencies",
        header: "Dependencies",
        cell: ({ row }) => row.dependencies.length,
        align: "center",
      },
      {
        id: "actions",
        header: "Actions",
        align: "right",
        cell: ({ row }) => (
          <div className="flex justify-end gap-2">
            <Button
              size="sm"
              variant="ghost"
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();
                onTaskEdit?.(row);
              }}
            >
              Edit
            </Button>
            <Button
              size="sm"
              variant="destructive"
              onClick={(event) => {
                event.preventDefault();
                event.stopPropagation();
                onTaskDelete?.(row);
              }}
            >
              Delete
            </Button>
          </div>
        ),
      },
    ],
    [onTaskDelete, onTaskEdit],
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="tasks-list">
      <h2>Tasks</h2>

      <DataTable
        columns={columns}
        data={tasks}
        emptyState="No tasks found"
        getRowId={(task) => task.id}
      />
    </div>
  );
};
