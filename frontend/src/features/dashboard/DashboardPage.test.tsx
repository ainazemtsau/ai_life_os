/**
 * Tests for DashboardPage component
 * Module: frontend.dashboard
 */

import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { DashboardPage } from "./DashboardPage";

describe("DashboardPage", () => {
  it("renders with greeting message", () => {
    render(<DashboardPage />);

    // Should have a greeting
    const greeting = screen.getByRole("heading", { level: 1 });
    expect(greeting).toBeInTheDocument();
    expect(greeting.textContent).toMatch(/welcome|hello|hi/i);
  });

  it("displays placeholder information", () => {
    render(<DashboardPage />);

    // Should have welcome message explaining the application purpose
    const aiLifeOSElements = screen.getAllByText(/AI Life OS/i);
    expect(aiLifeOSElements.length).toBeGreaterThan(0);

    // Should have description of available and upcoming features
    expect(screen.getByText(/Available Features:/i)).toBeInTheDocument();
    expect(screen.getByText(/Upcoming Features:/i)).toBeInTheDocument();
  });

  it("includes navigation link to Goals", () => {
    render(<DashboardPage />);

    // Should have a link/button to Goals page
    const goalsLink = screen.getByRole("link", { name: /goals/i });
    expect(goalsLink).toBeInTheDocument();
    expect(goalsLink).toHaveAttribute("href", "/goals");
  });

  it("accepts and uses className prop correctly", () => {
    const { container } = render(<DashboardPage className="custom-class" />);

    // The main container should have the custom class
    const mainElement = container.firstChild as HTMLElement;
    expect(mainElement.className).toContain("custom-class");
  });
});
