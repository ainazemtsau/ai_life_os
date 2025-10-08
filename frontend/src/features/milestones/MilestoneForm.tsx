import React, { useState, useEffect } from "react";

// Adjust import based on your design system
import type { Goal } from "@/features/goals/types"; // Adjust import path as needed
import type { Milestone } from "@/features/milestones/types"; // Assuming a types file exists or will be created

interface MilestoneFormProps {
  milestone?: Milestone; // If provided, form is in edit mode
  onSubmit: (milestone: Milestone) => void;
  onCancel: () => void;
  goals: Goal[]; // Available goals for the goal selector
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
  error?: string;
  goals: Goal[];
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ value, error, goals, onChange }) => (
  <div className="form-group">
    <label htmlFor="goal_id">Goal:</label>
    <select
      id="goal_id"
      name="goal_id"
      value={value}
      onChange={onChange}
      className={error ? "error" : ""}
    >
      <option value="">Select a Goal</option>
      {goals.map((goal) => (
        <option key={goal.id} value={goal.id}>
          {goal.title}
        </option>
      ))}
    </select>
    {error && <span className="error-message">{error}</span>}
  </div>
);

const DueDateField: React.FC<{
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}> = ({ value, onChange }) => (
  <div className="form-group">
    <label htmlFor="due">Due Date:</label>
    <input
      type="date"
      id="due"
      name="due"
      value={value ? value.split("T")[0] : ""}
      onChange={onChange}
    />
  </div>
);

const StatusField: React.FC<{
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}> = ({ value, onChange }) => (
  <div className="form-group">
    <label htmlFor="status">Status:</label>
    <select id="status" name="status" value={value} onChange={onChange}>
      <option value="todo">To Do</option>
      <option value="doing">Doing</option>
      <option value="done">Done</option>
      <option value="blocked">Blocked</option>
    </select>
  </div>
);

const DemoCriterionField: React.FC<{
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
}> = ({ value, onChange }) => (
  <div className="form-group">
    <label htmlFor="demo_criterion">Demo Criterion:</label>
    <textarea id="demo_criterion" name="demo_criterion" value={value} onChange={onChange} />
  </div>
);

const BlockingField: React.FC<{
  checked: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}> = ({ checked, onChange }) => (
  <div className="form-group">
    <label>
      <input type="checkbox" name="blocking" checked={checked} onChange={onChange} />
      Blocking
    </label>
  </div>
);

// Helper functions
const getInitialFormData = (
  milestone?: Milestone,
): Omit<Milestone, "id" | "created_at" | "updated_at"> => {
  if (!milestone) {
    return { title: "", goal_id: "", due: "", status: "todo", demo_criterion: "", blocking: false };
  }
  return {
    title: milestone.title,
    goal_id: milestone.goal_id,
    due: milestone.due || "",
    status: milestone.status,
    demo_criterion: milestone.demo_criterion,
    blocking: milestone.blocking,
  };
};

const validateFormData = (
  formData: Omit<Milestone, "id" | "created_at" | "updated_at">,
): Record<string, string> => {
  const newErrors: Record<string, string> = {};
  if (!formData.title.trim()) {
    newErrors["title"] = "Title is required";
  }
  if (!formData.goal_id) {
    newErrors["goal_id"] = "Goal is required";
  }
  return newErrors;
};

const createMilestoneData = (
  formData: Omit<Milestone, "id" | "created_at" | "updated_at">,
  milestone?: Milestone,
): Milestone => ({
  ...formData,
  id: milestone?.id || "",
  created_at: milestone?.created_at || new Date().toISOString(),
  updated_at: new Date().toISOString(),
});

export const MilestoneForm: React.FC<MilestoneFormProps> = ({
  milestone,
  onSubmit,
  onCancel,
  goals,
}) => {
  const isEditMode = !!milestone;
  const [formData, setFormData] = useState(() => getInitialFormData(milestone));
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (milestone) {
      setFormData(getInitialFormData(milestone));
    }
  }, [milestone]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const { name, value, type } = e.target;
    const val = type === "checkbox" ? (e.target as HTMLInputElement).checked : value;
    setFormData((prev) => ({ ...prev, [name as keyof typeof formData]: val }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors = validateFormData(formData);
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    onSubmit(createMilestoneData(formData, milestone));
  };

  return (
    <form onSubmit={handleSubmit} className="milestone-form">
      <h2>{isEditMode ? "Edit Milestone" : "Create Milestone"}</h2>

      <TitleField
        value={formData.title}
        {...(errors["title"] && { error: errors["title"] })}
        onChange={handleChange}
      />
      <GoalField
        value={formData.goal_id}
        {...(errors["goal_id"] && { error: errors["goal_id"] })}
        goals={goals}
        onChange={handleChange}
      />
      <DueDateField value={formData.due || ""} onChange={handleChange} />
      <StatusField value={formData.status} onChange={handleChange} />
      <DemoCriterionField value={formData.demo_criterion} onChange={handleChange} />
      <BlockingField checked={formData.blocking} onChange={handleChange} />

      <div className="form-actions">
        <button type="submit">Save</button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
};
