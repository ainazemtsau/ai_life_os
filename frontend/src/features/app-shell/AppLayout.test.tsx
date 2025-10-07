/**
 * Tests for AppLayout component
 * Module: frontend.app-shell
 */

import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { AppLayout } from "./AppLayout";

describe("AppLayout", () => {
  it("renders children correctly", () => {
    render(
      <AppLayout>
        <div data-testid="test-child">Test Content</div>
      </AppLayout>,
    );

    const child = screen.getByTestId("test-child");
    expect(child).toBeInTheDocument();
    expect(child.textContent).toBe("Test Content");
  });

  it("applies dark theme by default", () => {
    const { container } = render(
      <AppLayout>
        <div>Content</div>
      </AppLayout>,
    );

    // The layout should have dark theme applied (dark class or data-theme attribute)
    const layoutElement = container.firstChild as HTMLElement;
    expect(
      layoutElement.className.includes("dark") ||
        layoutElement.getAttribute("data-theme") === "dark",
    ).toBe(true);
  });

  it("accepts and uses className prop correctly", () => {
    const { container } = render(
      <AppLayout className="custom-class">
        <div>Content</div>
      </AppLayout>,
    );

    const layoutElement = container.firstChild as HTMLElement;
    expect(layoutElement.className).toContain("custom-class");
  });

  it("has correct layout structure", () => {
    const { container } = render(
      <AppLayout>
        <div data-testid="test-content">Test Content</div>
      </AppLayout>,
    );

    // Layout should wrap children properly
    expect(container.firstChild).toBeInTheDocument();
    expect(screen.getByTestId("test-content")).toBeInTheDocument();
  });
});
