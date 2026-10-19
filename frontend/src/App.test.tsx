import { render, screen } from "@testing-library/react";
import { describe, it, expect, beforeEach } from "vitest";
import App from "./App";
import { __setSignalServiceForTests } from "./services/provider";
import { MockSignalService } from "./services/MockSignalService";

describe("App shell", () => {
  beforeEach(() => {
    __setSignalServiceForTests(new MockSignalService());
  });

  it("renders the sidebar links", () => {
    render(<App />);
    expect(screen.getByRole("link", { name: "Competitors" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Briefing" })).toBeInTheDocument();
  });

  it("renders the page title", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "SignalStack" })).toBeInTheDocument();
  });

  it("renders the competitors page at /", async () => {
    render(<App />);
    expect(await screen.findByRole("heading", { name: "Competitors" })).toBeInTheDocument();
  });
});