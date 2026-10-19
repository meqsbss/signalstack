import { describe, it, expect, beforeEach } from "vitest";
import { MockSignalService } from "./MockSignalService";

describe("MockSignalService", () => {
  let svc: MockSignalService;

  beforeEach(() => {
    svc = new MockSignalService();
  });

  it("lists seeded competitors sorted by name", async () => {
    const list = await svc.listCompetitors();
    expect(list.map((c) => c.name)).toEqual([
      "Acme Analytics",
      "Flowdesk",
      "Nimbus CRM",
    ]);
  });

  it("adds a competitor", async () => {
    const c = await svc.addCompetitor({
      name: "Test Co",
      domain: "test.co",
    });
    expect(c.id).toBeTruthy();
    const list = await svc.listCompetitors();
    expect(list.some((x) => x.name === "Test Co")).toBe(true);
  });

  it("deletes a competitor and its events", async () => {
    await svc.deleteCompetitor("c1");
    const list = await svc.listCompetitors();
    expect(list.find((x) => x.id === "c1")).toBeUndefined();
    const events = await svc.listChangeEvents("c1");
    expect(events).toEqual([]);
  });

  it("refresh returns events for the competitor", async () => {
    const events = await svc.refreshCompetitor("c1");
    expect(events.length).toBeGreaterThan(0);
    expect(events.every((e) => e.competitor_id === "c1")).toBe(true);
  });

  it("acknowledges an event", async () => {
    const e = await svc.acknowledgeChangeEvent("e1");
    expect(e.acknowledged).toBe(true);
  });

  it("returns revenue context or null", async () => {
    expect(await svc.getRevenueContext("c1")).not.toBeNull();
    expect(await svc.getRevenueContext("c3")).toBeNull();
  });

  it("returns null before any briefing is generated", async () => {
    expect(await svc.getLatestBriefing()).toBeNull();
  });

  it("generates a briefing with high-severity event first", async () => {
    const b = await svc.generateBriefing();
    expect(b.top_events[0].severity).toBe("high");
    expect(b.summary_text).toContain("changes across");
    const latest = await svc.getLatestBriefing();
    expect(latest?.id).toBe(b.id);
  });

  it("regenerating replaces the latest briefing", async () => {
    const b1 = await svc.generateBriefing();
    const b2 = await svc.generateBriefing();
    const latest = await svc.getLatestBriefing();
    expect(latest?.id).toBe(b2.id);
    expect(latest?.id).not.toBe(b1.id);
  });
});