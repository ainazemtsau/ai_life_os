import React from "react";

import { Button, DataTable, type DataTableColumn } from "@/features/design";
import type { Project } from "@/features/projects/types";

import { useProjects } from "./hooks";

const formatEnumLabel = (value: unknown): React.ReactNode => {
  if (typeof value === "string" && value.length > 0) {
    return value.charAt(0).toUpperCase() + value.slice(1);
  }

  if (value === null || value === undefined) {
    return <span className="text-muted-foreground">—</span>;
  }

  return String(value);
};

interface ProjectsListProps {
  onProjectEdit?: (project: Project) => void;
  onProjectDelete?: (project: Project) => void;
  filterByGoal?: string;
}

export const ProjectsList: React.FC<ProjectsListProps> = ({
  onProjectEdit,
  onProjectDelete,
  filterByGoal,
}) => {
  // Using the hook to get projects data
  const { projects, loading, error } = useProjects(filterByGoal);

  const columns = React.useMemo<DataTableColumn<Project>[]>(
    () => [
      {
        id: "title",
        header: "Title",
        accessor: "title",
      },
      {
        id: "goal",
        header: "Goal",
        cell: ({ row }) =>
          row.goal_id ? row.goal_id : <span className="text-muted-foreground">—</span>,
      },
      {
        id: "status",
        header: "Status",
        cell: ({ row }) => (
          <span className={`status-${row.status}`}>
            {row.status.charAt(0).toUpperCase() + row.status.slice(1)}
          </span>
        ),
      },
      {
        id: "priority",
        header: "Priority",
        accessor: (project) => project.priority,
        cell: ({ value }) => formatEnumLabel(value),
      },
      {
        id: "risk",
        header: "Risk",
        accessor: (project) => project.risk,
        cell: ({ value }) => formatEnumLabel(value),
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
                onProjectEdit?.(row);
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
                onProjectDelete?.(row);
              }}
            >
              Delete
            </Button>
          </div>
        ),
      },
    ],
    [onProjectDelete, onProjectEdit],
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="projects-list">
      <h2>Projects</h2>

      <DataTable
        columns={columns}
        data={projects}
        emptyState="No projects found"
        getRowId={(project) => project.id}
      />
    </div>
  );
};
