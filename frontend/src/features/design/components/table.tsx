import * as React from "react";

import { cn } from "../utils/cn";

type Align = "left" | "center" | "right";

type Accessor<TData> = keyof TData | ((row: TData) => unknown);

export interface DataTableColumnHeaderContext<TData> {
  column: DataTableColumn<TData>;
}

export interface DataTableCellContext<TData> {
  column: DataTableColumn<TData>;
  row: TData;
  rowIndex: number;
  value: unknown;
}

export interface DataTableColumn<TData> {
  id: string;
  header: React.ReactNode | ((context: DataTableColumnHeaderContext<TData>) => React.ReactNode);
  accessor?: Accessor<TData>;
  cell?: (context: DataTableCellContext<TData>) => React.ReactNode;
  align?: Align;
  className?: string;
  headerClassName?: string;
  width?: string | number;
  minWidth?: string | number;
}

export interface DataTableProps<TData> {
  data: TData[];
  columns: DataTableColumn<TData>[];
  emptyState?: React.ReactNode;
  caption?: React.ReactNode;
  toolbar?: React.ReactNode;
  getRowId?: (row: TData, index: number) => string | number;
  className?: string;
  wrapperClassName?: string;
  rowClassName?: string | ((row: TData, index: number) => string | undefined);
  onRowClick?: (row: TData, index: number) => void;
}

function alignClassName(align?: Align): string {
  if (align === "center") {
    return "text-center";
  }
  if (align === "right") {
    return "text-right";
  }
  return "text-left";
}

function resolveRowKey<TData>(
  row: TData,
  index: number,
  getRowId?: (row: TData, index: number) => string | number,
): string {
  const provided = getRowId?.(row, index);
  if (provided !== undefined) {
    return typeof provided === "number" ? `row-${provided}` : String(provided);
  }

  const candidate = (row as { id?: string | number }).id;
  if (candidate !== undefined) {
    return typeof candidate === "number" ? `row-${candidate}` : String(candidate);
  }

  return `row-${index}`;
}

function extractValue<TData>(row: TData, column: DataTableColumn<TData>): unknown {
  if (column.accessor) {
    if (typeof column.accessor === "function") {
      return column.accessor(row);
    }

    return (row as Record<string, unknown>)[column.accessor as string];
  }

  if (column.id in (row as Record<string, unknown>)) {
    return (row as Record<string, unknown>)[column.id];
  }

  return undefined;
}

function isPrimitiveValue(value: unknown): value is string | number | boolean {
  return typeof value === "string" || typeof value === "number" || typeof value === "boolean";
}

function renderPrimitiveValue(value: string | number | boolean): React.ReactNode {
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }
  return value;
}

function renderDefaultCell(value: unknown): React.ReactNode {
  if (value === null || value === undefined) {
    return <span className="text-muted-foreground">—</span>;
  }

  if (React.isValidElement(value)) {
    return value;
  }

  if (Array.isArray(value)) {
    return value.length;
  }

  if (isPrimitiveValue(value)) {
    return renderPrimitiveValue(value);
  }

  return String(value);
}

function resolveRowClassName<TData>(
  row: TData,
  index: number,
  rowClassName?: string | ((row: TData, index: number) => string | undefined),
): string | undefined {
  if (typeof rowClassName === "function") {
    return rowClassName(row, index);
  }
  return rowClassName;
}

export function DataTable<TData>({
  data,
  columns,
  emptyState = "No data to display",
  caption,
  toolbar,
  getRowId,
  className,
  wrapperClassName,
  rowClassName,
  onRowClick,
}: DataTableProps<TData>) {
  return (
    <div className={cn("space-y-3", wrapperClassName)}>
      {toolbar ? (
        <div className="flex flex-wrap items-center justify-between gap-2">{toolbar}</div>
      ) : null}
      <div className="overflow-hidden rounded-xl border border-border bg-card shadow-sm">
        <div className="relative w-full overflow-x-auto">
          <table className={cn("w-full caption-bottom text-sm text-foreground", className)}>
            {caption ? (
              <caption className="px-4 pt-6 pb-4 text-left text-sm text-muted-foreground">
                {caption}
              </caption>
            ) : null}
            <thead className="bg-muted/50 text-muted-foreground">
              <tr>
                {columns.map((column) => (
                  <th
                    key={column.id}
                    className={cn(
                      "h-12 px-4 text-left align-middle text-sm font-medium",
                      alignClassName(column.align),
                      column.headerClassName,
                    )}
                    style={{ width: column.width, minWidth: column.minWidth }}
                    scope="col"
                  >
                    {typeof column.header === "function"
                      ? column.header({ column })
                      : column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.length === 0 ? (
                <tr>
                  <td
                    className="px-4 py-10 text-center text-sm text-muted-foreground"
                    colSpan={columns.length}
                  >
                    {emptyState}
                  </td>
                </tr>
              ) : (
                data.map((row, index) => {
                  const key = resolveRowKey(row, index, getRowId);
                  const rowClasses = cn(
                    "border-t border-border/60 transition-colors hover:bg-muted/40",
                    resolveRowClassName(row, index, rowClassName),
                    onRowClick && "cursor-pointer",
                  );

                  return (
                    <tr
                      key={key}
                      className={rowClasses}
                      onClick={onRowClick ? () => onRowClick(row, index) : undefined}
                    >
                      {columns.map((column) => {
                        const value = extractValue(row, column);
                        const content =
                          column.cell?.({
                            column,
                            row,
                            rowIndex: index,
                            value,
                          }) ?? renderDefaultCell(value);

                        return (
                          <td
                            key={column.id}
                            className={cn(
                              "px-4 py-3 align-middle text-sm text-foreground",
                              alignClassName(column.align),
                              column.className,
                            )}
                          >
                            {content}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
