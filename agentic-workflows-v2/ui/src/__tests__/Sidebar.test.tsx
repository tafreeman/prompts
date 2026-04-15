import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import Sidebar from "../components/layout/Sidebar";

describe("Sidebar", () => {
  it("renders the main navigation links", () => {
    render(
      <MemoryRouter initialEntries={["/workflows"]}>
        <Sidebar />
      </MemoryRouter>
    );

    expect(screen.getByText("Agentic Workflows")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /dashboard/i })).toHaveAttribute("href", "/");
    expect(screen.getByRole("link", { name: /workflows/i })).toHaveAttribute("href", "/workflows");
    expect(screen.getByRole("link", { name: /datasets/i })).toHaveAttribute("href", "/datasets");
    expect(screen.getByRole("link", { name: /evaluations/i })).toHaveAttribute("href", "/evaluations");
    expect(screen.getByRole("link", { name: /live/i })).toHaveAttribute("href", "/live/latest");
  });
});
