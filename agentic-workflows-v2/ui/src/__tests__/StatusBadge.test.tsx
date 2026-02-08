import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import StatusBadge from "../components/common/StatusBadge";

describe("StatusBadge", () => {
  it("renders the correct label for each status", () => {
    const statuses = [
      { status: "pending", label: "Pending" },
      { status: "running", label: "Running" },
      { status: "success", label: "Success" },
      { status: "failed", label: "Failed" },
      { status: "skipped", label: "Skipped" },
      { status: "cancelled", label: "Cancelled" },
    ] as const;

    for (const { status, label } of statuses) {
      const { unmount } = render(<StatusBadge status={status} />);
      expect(screen.getByText(label)).toBeInTheDocument();
      unmount();
    }
  });

  it("falls back to Pending for unknown status", () => {
    render(<StatusBadge status="unknown" />);
    expect(screen.getByText("Pending")).toBeInTheDocument();
  });

  it("applies md size class", () => {
    const { container } = render(<StatusBadge status="success" size="md" />);
    const badge = container.firstElementChild;
    expect(badge?.className).toContain("text-sm");
  });
});
