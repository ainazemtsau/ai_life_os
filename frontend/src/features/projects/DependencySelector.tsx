import React from "react";

interface DependencyOption {
  id: string;
  title: string;
}

interface DependencySelectorProps {
  selectedDependencies: string[];
  availableDependencies: DependencyOption[];
  onChange: (selectedIds: string[]) => void;
  label?: string;
}

export const DependencySelector: React.FC<DependencySelectorProps> = ({
  selectedDependencies,
  availableDependencies,
  onChange,
  label = "Dependencies",
}) => {
  const handleToggle = (id: string) => {
    if (selectedDependencies.includes(id)) {
      // Remove if already selected
      onChange(selectedDependencies.filter((depId) => depId !== id));
    } else {
      // Add if not selected
      onChange([...selectedDependencies, id]);
    }
  };

  return (
    <div className="dependency-selector">
      <label>{label}:</label>
      <div className="dependency-options">
        {availableDependencies.map((dep) => (
          <div key={dep.id} className="dependency-option">
            <label>
              <input
                type="checkbox"
                checked={selectedDependencies.includes(dep.id)}
                onChange={() => handleToggle(dep.id)}
              />
              {dep.title}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};
