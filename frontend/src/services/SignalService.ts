import type {
  AddCompetitorInput,
  Briefing,
  ChangeEvent,
  Competitor,
  RevenueContext,
} from "../types";

export interface SignalService {
  listCompetitors(): Promise<Competitor[]>;
  getCompetitor(id: string): Promise<Competitor>;
  addCompetitor(input: AddCompetitorInput): Promise<Competitor>;
  deleteCompetitor(id: string): Promise<void>;

  refreshCompetitor(id: string): Promise<ChangeEvent[]>;
  listChangeEvents(competitorId: string): Promise<ChangeEvent[]>;
  acknowledgeChangeEvent(eventId: string): Promise<ChangeEvent>;

  getRevenueContext(competitorId: string): Promise<RevenueContext | null>;

  getLatestBriefing(): Promise<Briefing | null>;
  generateBriefing(): Promise<Briefing>;
}