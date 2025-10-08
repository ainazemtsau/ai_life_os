import React from "react";

import { Button, DataTable, type DataTableColumn } from "@/features/design";
import type { Milestone } from "@/features/milestones/types";

import { useMilestones } from "./hooks";

interface MilestonesListProps {
  onMilestoneEdit?: (milestone: Milestone) => void;
  onMilestoneDelete?: (milestone: Milestone) => void;
  filterByGoal?: string;
}

export const MilestonesList: React.FC<MilestonesListProps> = ({
  onMilestoneEdit,
  onMilestoneDelete,
  filterByGoal,
}) => {
  // Using the hook to get milestones data
  const { milestones, loading, error } = useMilestones(filterByGoal);

  const columns = React.useMemo<DataTableColumn<Milestone>[]>(
    () => [
      {
        id: "title",
        header: "Title",
        accessor: "title",
      },
      {
        id: "goal",
        header: "Goal",
        accessor: (milestone) => milestone.goal_id,
      },
      {
        id: "dueDate",
        header: "Due Date",
        accessor: (milestone) => milestone.due,
        cell: ({ value }) => {
          if (typeof value !== "string" || value.length === 0) {
            return <span className="text-muted-foreground">—</span>;
          }
          const date = new Date(value);
          if (Number.isNaN(date.getTime())) {
            return <span className="text-muted-foreground">—</span>;
          }
          const isoDate = value.split("T")[0];
          return isoDate ?? date.toISOString().split("T")[0];
        },
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
        id: "blocking",
        header: "Blocking",
        accessor: (milestone) => milestone.blocking,
        cell: ({ row }) => (row.blocking ? "Yes" : "No"),
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
                onMilestoneEdit?.(row);
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
                onMilestoneDelete?.(row);
              }}
            >
              Delete
            </Button>
          </div>
        ),
      },
    ],
    [onMilestoneDelete, onMilestoneEdit],
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="milestones-list">
      <h2>Milestones</h2>

      <DataTable
        columns={columns}
        data={milestones}
        emptyState="No milestones found"
        getRowId={(milestone) => milestone.id}
      />
    </div>
  );
};
