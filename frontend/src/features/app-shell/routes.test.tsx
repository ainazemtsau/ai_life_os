/**
 * Tests for route components
 * Module: frontend.app-shell
 */

import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { DashboardRoute, GoalsRoute } from "./routes";

describe("DashboardRoute", () => {
  it("renders DashboardPage component", () => {
    render(<DashboardRoute />);

    // Should render dashboard content
    // We look for the dashboard's welcome text
    expect(screen.getByText(/Welcome to AI Life OS/i)).toBeInTheDocument();
  });

  it("renders without errors", () => {
    const { container } = render(<DashboardRoute />);
    expect(container.firstChild).toBeInTheDocument();
  });
});

describe("GoalsRoute", () => {
  it("renders without errors", () => {
    const { container } = render(<GoalsRoute />);
    expect(container.firstChild).toBeInTheDocument();
  });

  it("renders goals page content", () => {
    render(<GoalsRoute />);

    // Should render goals-related content
    // The goals module should provide its page component
    const mainElement = screen.getByRole("main");
    expect(mainElement).toBeInTheDocument();
  });
});
