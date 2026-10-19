import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { describe, it, expect } from "vitest";
import Shell from "./Shell";

describe("Shell", () => {
  it("marks the active sidebar link", () => {
    render(
      <MemoryRouter initialEntries={["/briefing"]}>
        <Routes>
          <Route element={<Shell />}>
            <Route path="/briefing" element={<div>briefing content</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    const briefingLink = screen.getByRole("link", { name: "Briefing" });
    const competitorsLink = screen.getByRole("link", { name: "Competitors" });
    expect(briefingLink).toHaveAttribute("aria-current", "page");
    expect(competitorsLink).not.toHaveAttribute("aria-current");
  });

  it("renders children through Outlet", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route element={<Shell />}>
            <Route path="/" element={<div>home content</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByText("home content")).toBeInTheDocument();
  });
});