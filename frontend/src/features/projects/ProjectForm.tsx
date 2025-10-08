import React, { useState, useEffect } from "react";

import type { Goal } from "@/features/goals/types"; // Adjust import path as needed
import type { Project } from "@/features/projects/types";

import { DependencySelector } from "./DependencySelector";

interface ProjectFormProps {
  project?: Project; // If provided, form is in edit mode
  onSubmit: (project: Project) => void;
  onCancel: () => void;
  goals: Goal[]; // Available goals for the goal selector
  projects: Project[]; // Available projects for the dependency selector (same goal)
}

// Field components
const TitleField: React.FC<{
  value: string;
  error?: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}> = ({ value, error, onChange }) => (
  <div className="form-group">
    <label htmlFor="title">Title:</label>
    <input
      type="text"
      id="title"
      name="title"
      value={value}
      onChange={onChange}
      className={error ? "error" : ""}
    />
    {error && <span className="error-message">{error}</span>}
  </div>
);

const GoalField: React.FC<{
  value: string;
  goals: Goal[];
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ value, goals, onChange }) => (
  <div className="form-group">
    <label htmlFor="goal_id">Goal:</label>
    <select id="goal_id" name="goal_id" value={value} onChange={onChange}>
      <option value="">No Goal</option>
      {goals.map((goal) => (
        <option key={goal.id} value={goal.id}>
          {goal.title}
        </option>
      ))}
    </select>
  </div>
);

const StatusPriorityFields: React.FC<{
  status: string;
  priority: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ status, priority, onChange }) => (
  <>
    <div className="form-group">
      <label htmlFor="status">Status:</label>
      <select id="status" name="status" value={status} onChange={onChange}>
        <option value="todo">To Do</option>
        <option value="doing">Doing</option>
        <option value="done">Done</option>
        <option value="blocked">Blocked</option>
      </select>
    </div>

    <div className="form-group">
      <label htmlFor="priority">Priority:</label>
      <select id="priority" name="priority" value={priority} onChange={onChange}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
        <option value="critical">Critical</option>
      </select>
    </div>
  </>
);

const RiskScopeFields: React.FC<{
  risk: string;
  scope: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement | HTMLTextAreaElement>) => void;
}> = ({ risk, scope, onChange }) => (
  <>
    <div className="form-group">
      <label htmlFor="risk">Risk:</label>
      <select id="risk" name="risk" value={risk} onChange={onChange}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>

    <div className="form-group">
      <label htmlFor="scope">Scope:</label>
      <textarea id="scope" name="scope" value={scope} onChange={onChange} />
    </div>
  </>
);

// Helper functions
const getInitialFormData = (
  project?: Project,
): Omit<Project, "id" | "created_at" | "updated_at"> => {
  if (!project) {
    return {
      title: "",
      status: "todo",
      priority: "medium",
      risk: "medium",
      dependencies: [],
    };
  }
  const data: Omit<Project, "id" | "created_at" | "updated_at"> = {
    title: project.title,
    status: project.status,
    priority: project.priority,
    risk: project.risk,
    dependencies: project.dependencies,
  };
  if (project.goal_id !== undefined) {
    data.goal_id = project.goal_id;
  }
  if (project.scope !== undefined) {
    data.scope = project.scope;
  }
  return data;
};

const validateFormData = (
  formData: Omit<Project, "id" | "created_at" | "updated_at">,
): Record<string, string> => {
  const newErrors: Record<string, string> = {};
  if (!formData.title.trim()) {
    newErrors["title"] = "Title is required";
  }
  return newErrors;
};

const filterSameGoalProjects = (projects: Project[], goalId: string, currentProjectId?: string) =>
  projects.filter((p) => p.goal_id === goalId && p.id !== currentProjectId);

const createProjectData = (
  formData: Omit<Project, "id" | "created_at" | "updated_at">,
  sameGoalProjects: Project[],
  project?: Project,
): Project => ({
  ...formData,
  id: project?.id || "",
  created_at: project?.created_at || new Date().toISOString(),
  updated_at: new Date().toISOString(),
  dependencies: formData.dependencies.filter((id) => sameGoalProjects.some((p) => p.id === id)),
});

export const ProjectForm: React.FC<ProjectFormProps> = ({
  project,
  onSubmit,
  onCancel,
  goals,
  projects,
}) => {
  const isEditMode = !!project;
  const [formData, setFormData] = useState(() => getInitialFormData(project));
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (project) {
      setFormData(getInitialFormData(project));
    }
  }, [project]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleDependenciesChange = (selectedIds: string[]) => {
    setFormData((prev) => ({ ...prev, dependencies: selectedIds }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors = validateFormData(formData);
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    const sameGoalProjects = filterSameGoalProjects(projects, formData.goal_id || "", project?.id);
    onSubmit(createProjectData(formData, sameGoalProjects, project));
  };

  const availableDependencies = filterSameGoalProjects(
    projects,
    formData.goal_id || "",
    project?.id,
  );

  return (
    <form onSubmit={handleSubmit} className="project-form">
      <h2>{isEditMode ? "Edit Project" : "Create Project"}</h2>

      <TitleField
        value={formData.title}
        {...(errors["title"] && { error: errors["title"] })}
        onChange={handleChange}
      />
      <GoalField value={formData.goal_id || ""} goals={goals} onChange={handleChange} />
      <StatusPriorityFields
        status={formData.status}
        priority={formData.priority}
        onChange={handleChange}
      />
      <RiskScopeFields risk={formData.risk} scope={formData.scope || ""} onChange={handleChange} />

      <div className="form-group">
        <DependencySelector
          selectedDependencies={formData.dependencies}
          availableDependencies={availableDependencies.map((p) => ({ id: p.id, title: p.title }))}
          onChange={handleDependenciesChange}
          label="Dependencies (within same goal)"
        />
      </div>

      <div className="form-actions">
        <button type="submit">Save</button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
};
