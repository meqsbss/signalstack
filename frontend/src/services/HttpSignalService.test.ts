import { describe, it, expect, vi, beforeEach } from "vitest";
import { HttpSignalService } from "./HttpSignalService";
import { ApiError } from "../types";

const mockFetch = vi.fn();
globalThis.fetch = mockFetch as unknown as typeof fetch;

function jsonResponse(data: unknown, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => data,
  } as Response;
}

describe("HttpSignalService", () => {
  let svc: HttpSignalService;
  beforeEach(() => {
    svc = new HttpSignalService();
    mockFetch.mockReset();
  });

  it("lists competitors", async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse([{ id: "1", name: "A" }]));
    const r = await svc.listCompetitors();
    expect(r[0].name).toBe("A");
  });

  it("throws ApiError on 4xx", async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse({ detail: "bad" }, 422));
    await expect(svc.getCompetitor("x")).rejects.toBeInstanceOf(ApiError);
  });

  it("returns null for 404 latest briefing", async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse({ detail: "none" }, 404));
    const r = await svc.getLatestBriefing();
    expect(r).toBeNull();
  });

  it("posts add competitor", async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse({ id: "1", name: "A" }, 201));
    const r = await svc.addCompetitor({ name: "A", domain: "a.com" });
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/competitors"),
      expect.objectContaining({ method: "POST" })
    );
    expect(r.id).toBe("1");
  });
});