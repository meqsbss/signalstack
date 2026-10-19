import type {
  AddCompetitorInput,
  Briefing,
  ChangeEvent,
  Competitor,
  RevenueContext,
} from "../types";
import { ApiError } from "../types";
import type { SignalService } from "./SignalService";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8091";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    let body: unknown = null;
    try {
      body = await res.json();
    } catch {
      /* ignore */
    }
    throw new ApiError(res.status, body);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export class HttpSignalService implements SignalService {
  listCompetitors() {
    return request<Competitor[]>("/competitors");
  }
  getCompetitor(id: string) {
    return request<Competitor>(`/competitors/${id}`);
  }
  addCompetitor(input: AddCompetitorInput) {
    return request<Competitor>("/competitors", {
      method: "POST",
      body: JSON.stringify(input),
    });
  }
  async deleteCompetitor(id: string) {
    await request<void>(`/competitors/${id}`, { method: "DELETE" });
  }
  refreshCompetitor(id: string) {
    return request<ChangeEvent[]>(`/competitors/${id}/refresh`, { method: "POST" });
  }
  listChangeEvents(competitorId: string) {
    return request<ChangeEvent[]>(`/competitors/${competitorId}/changes`);
  }
  acknowledgeChangeEvent(eventId: string) {
    return request<ChangeEvent>(`/events/${eventId}/acknowledge`, { method: "POST" });
  }
  getRevenueContext(competitorId: string) {
    return request<RevenueContext | null>(`/competitors/${competitorId}/revenue`);
  }
  async getLatestBriefing() {
    try {
      return await request<Briefing>("/briefings/latest");
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) return null;
      throw e;
    }
  }
  generateBriefing() {
    return request<Briefing>("/briefings/generate", { method: "POST" });
  }
}