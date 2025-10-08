import React, { useState, useEffect } from "react";

import type { Task } from "@/features/projects/types";
import type { Project } from "@/features/projects/types";

import { DependencySelector } from "./DependencySelector";

interface TaskFormProps {
  task?: Task; // If provided, form is in edit mode
  onSubmit: (task: Task) => void;
  onCancel: () => void;
  projects: Project[]; // Available projects for the project selector
  tasks: Task[]; // Available tasks for the dependency selector (same project)
}

// Field components
const TitleProjectFields: React.FC<{
  title: string;
  projectId: string;
  titleError?: string;
  projectError?: string;
  projects: Project[];
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
}> = ({ title, projectId, titleError, projectError, projects, onChange }) => (
  <>
    <div className="form-group">
      <label htmlFor="title">Title:</label>
      <input
        type="text"
        id="title"
        name="title"
        value={title}
        onChange={onChange}
        className={titleError ? "error" : ""}
      />
      {titleError && <span className="error-message">{titleError}</span>}
    </div>

    <div className="form-group">
      <label htmlFor="project_id">Project:</label>
      <select
        id="project_id"
        name="project_id"
        value={projectId}
        onChange={onChange}
        className={projectError ? "error" : ""}
      >
        <option value="">Select a Project</option>
        {projects.map((project) => (
          <option key={project.id} value={project.id}>
            {project.title}
          </option>
        ))}
      </select>
      {projectError && <span className="error-message">{projectError}</span>}
    </div>
  </>
);

const StatusSizeFields: React.FC<{
  status: string;
  size: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ status, size, onChange }) => (
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
      <label htmlFor="size">Size:</label>
      <select id="size" name="size" value={size} onChange={onChange}>
        <option value="tiny">Tiny</option>
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
        <option value="xlarge">X-Large</option>
      </select>
    </div>
  </>
);

const EnergyRiskFields: React.FC<{
  energy: string;
  risk: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ energy, risk, onChange }) => (
  <>
    <div className="form-group">
      <label htmlFor="energy">Energy:</label>
      <select id="energy" name="energy" value={energy} onChange={onChange}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>

    <div className="form-group">
      <label htmlFor="risk">Risk:</label>
      <select id="risk" name="risk" value={risk} onChange={onChange}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>
  </>
);

const ContinuityClarityFields: React.FC<{
  continuity: string;
  clarity: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ continuity, clarity, onChange }) => (
  <>
    <div className="form-group">
      <label htmlFor="continuity">Continuity:</label>
      <select id="continuity" name="continuity" value={continuity} onChange={onChange}>
        <option value="discrete">Discrete</option>
        <option value="recurring">Recurring</option>
      </select>
    </div>

    <div className="form-group">
      <label htmlFor="clarity">Clarity:</label>
      <select id="clarity" name="clarity" value={clarity} onChange={onChange}>
        <option value="unclear">Unclear</option>
        <option value="fuzzy">Fuzzy</option>
        <option value="clear">Clear</option>
      </select>
    </div>
  </>
);

// Helper functions
const getInitialFormData = (task?: Task): Omit<Task, "id" | "created_at" | "updated_at"> => {
  if (!task) {
    return {
      title: "",
      project_id: "",
      status: "todo",
      size: "medium",
      energy: "medium",
      continuity: "discrete",
      clarity: "fuzzy",
      risk: "medium",
      dependencies: [],
    };
  }
  return {
    title: task.title,
    project_id: task.project_id,
    status: task.status,
    size: task.size,
    energy: task.energy,
    continuity: task.continuity,
    clarity: task.clarity,
    risk: task.risk,
    dependencies: task.dependencies,
  };
};

const validateFormData = (
  formData: Omit<Task, "id" | "created_at" | "updated_at">,
): Record<string, string> => {
  const newErrors: Record<string, string> = {};
  if (!formData.title.trim()) {
    newErrors["title"] = "Title is required";
  }
  if (!formData.project_id) {
    newErrors["project_id"] = "Project is required";
  }
  return newErrors;
};

const filterSameProjectTasks = (tasks: Task[], projectId: string, currentTaskId?: string) =>
  tasks.filter((t) => t.project_id === projectId && t.id !== currentTaskId);

const createTaskData = (
  formData: Omit<Task, "id" | "created_at" | "updated_at">,
  sameProjectTasks: Task[],
  task?: Task,
): Task => ({
  ...formData,
  id: task?.id || "",
  created_at: task?.created_at || new Date().toISOString(),
  updated_at: new Date().toISOString(),
  dependencies: formData.dependencies.filter((id) => sameProjectTasks.some((t) => t.id === id)),
});

export const TaskForm: React.FC<TaskFormProps> = ({
  task,
  onSubmit,
  onCancel,
  projects,
  tasks,
}) => {
  const isEditMode = !!task;
  const [formData, setFormData] = useState(() => getInitialFormData(task));
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (task) {
      setFormData(getInitialFormData(task));
    }
  }, [task]);

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
    const sameProjectTasks = filterSameProjectTasks(tasks, formData.project_id, task?.id);
    onSubmit(createTaskData(formData, sameProjectTasks, task));
  };

  const availableDependencies = filterSameProjectTasks(tasks, formData.project_id, task?.id);

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <h2>{isEditMode ? "Edit Task" : "Create Task"}</h2>

      <TitleProjectFields
        title={formData.title}
        projectId={formData.project_id}
        {...(errors["title"] && { titleError: errors["title"] })}
        {...(errors["project_id"] && { projectError: errors["project_id"] })}
        projects={projects}
        onChange={handleChange}
      />
      <StatusSizeFields status={formData.status} size={formData.size} onChange={handleChange} />
      <EnergyRiskFields energy={formData.energy} risk={formData.risk} onChange={handleChange} />
      <ContinuityClarityFields
        continuity={formData.continuity}
        clarity={formData.clarity}
        onChange={handleChange}
      />

      <div className="form-group">
        <DependencySelector
          selectedDependencies={formData.dependencies}
          availableDependencies={availableDependencies.map((t) => ({ id: t.id, title: t.title }))}
          onChange={handleDependenciesChange}
          label="Dependencies (within same project)"
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
