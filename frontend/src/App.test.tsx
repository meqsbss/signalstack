import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App shell", () => {
  it("renders the sidebar links", () => {
    render(<App />);
    expect(screen.getByRole("link", { name: "Competitors" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Briefing" })).toBeInTheDocument();
  });

  it("renders the page title", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "SignalStack" })).toBeInTheDocument();
  });

  it("renders the competitors page at /", () => {
    render(<App />);
    expect(screen.getByText(/Competitors list goes here/i)).toBeInTheDocument();
  });
});