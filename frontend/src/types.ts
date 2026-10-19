export type SourceType = "pricing" | "changelog" | "homepage";
export type Severity = "low" | "medium" | "high";

export interface Competitor {
  id: string;
  name: string;
  domain: string;
  trustmrr_slug: string | null;
  created_at: string;
  last_refreshed_at: string | null;
}

export interface ChangeEvent {
  id: string;
  competitor_id: string;
  competitor_name: string;
  source_type: SourceType;
  diff_summary: string;
  diff_full: string;
  severity: Severity;
  detected_at: string;
  acknowledged: boolean;
}

export interface RevenueContext {
  competitor_id: string;
  mrr: number;
  growth_30d: number;
  verified_at: string;
  source: "trustmrr";
}

export interface Briefing {
  id: string;
  week_start: string;
  summary_text: string;
  top_events: ChangeEvent[];
  created_at: string;
}

export interface AddCompetitorInput {
  name: string;
  domain: string;
  trustmrr_slug?: string | null;
}

export class ApiError extends Error {
  status: number;
  body: unknown;
  constructor(status: number, body: unknown) {
    super(`API error ${status}`);
    this.status = status;
    this.body = body;
  }
}