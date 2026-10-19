import type {
  AddCompetitorInput,
  Briefing,
  ChangeEvent,
  Competitor,
  RevenueContext,
} from "../types";
import type { SignalService } from "./SignalService";

const delay = (ms = 300) => new Promise((r) => setTimeout(r, ms));
const uuid = () => crypto.randomUUID();
const nowIso = () => new Date().toISOString();
const daysAgoIso = (n: number) =>
  new Date(Date.now() - n * 24 * 60 * 60 * 1000).toISOString();

function seedCompetitors(): Competitor[] {
  return [
    {
      id: "c1",
      name: "Acme Analytics",
      domain: "acme-analytics.com",
      trustmrr_slug: "acme-analytics",
      created_at: daysAgoIso(30),
      last_refreshed_at: daysAgoIso(1),
    },
    {
      id: "c2",
      name: "Nimbus CRM",
      domain: "nimbuscrm.io",
      trustmrr_slug: "nimbus-crm",
      created_at: daysAgoIso(20),
      last_refreshed_at: daysAgoIso(2),
    },
    {
      id: "c3",
      name: "Flowdesk",
      domain: "flowdesk.app",
      trustmrr_slug: null,
      created_at: daysAgoIso(10),
      last_refreshed_at: null,
    },
  ];
}

function seedEvents(): ChangeEvent[] {
  return [
    {
      id: "e1",
      competitor_id: "c1",
      competitor_name: "Acme Analytics",
      source_type: "pricing",
      diff_summary: "Price for Pro plan changed from $29 to $39",
      diff_full:
        "- Pro plan: $29 / month\n+ Pro plan: $39 / month\n  Includes 10 seats\n  Includes API access",
      severity: "high",
      detected_at: daysAgoIso(1),
      acknowledged: false,
    },
    {
      id: "e2",
      competitor_id: "c1",
      competitor_name: "Acme Analytics",
      source_type: "changelog",
      diff_summary: "New section: AI Insights",
      diff_full:
        "+ ## AI Insights\n+ Automatically summarize weekly metrics.\n  ## Existing features\n  Dashboards",
      severity: "medium",
      detected_at: daysAgoIso(2),
      acknowledged: false,
    },
    {
      id: "e3",
      competitor_id: "c2",
      competitor_name: "Nimbus CRM",
      source_type: "homepage",
      diff_summary: "Hero copy wording changed",
      diff_full:
        "- The CRM for small teams\n+ The CRM that grows with you",
      severity: "low",
      detected_at: daysAgoIso(3),
      acknowledged: true,
    },
  ];
}

function seedRevenue(): RevenueContext[] {
  return [
    {
      competitor_id: "c1",
      mrr: 24500,
      growth_30d: 8.2,
      verified_at: daysAgoIso(1),
      source: "trustmrr",
    },
    {
      competitor_id: "c2",
      mrr: 12000,
      growth_30d: -3.1,
      verified_at: daysAgoIso(2),
      source: "trustmrr",
    },
  ];
}

export class MockSignalService implements SignalService {
  private competitors: Competitor[] = seedCompetitors();
  private events: ChangeEvent[] = seedEvents();
  private revenue: RevenueContext[] = seedRevenue();
  private briefings: Briefing[] = [];

  async listCompetitors(): Promise<Competitor[]> {
    await delay();
    return [...this.competitors].sort((a, b) => a.name.localeCompare(b.name));
  }

  async getCompetitor(id: string): Promise<Competitor> {
    await delay();
    const c = this.competitors.find((x) => x.id === id);
    if (!c) throw new Error(`Competitor ${id} not found`);
    return c;
  }

  async addCompetitor(input: AddCompetitorInput): Promise<Competitor> {
    await delay();
    const competitor: Competitor = {
      id: uuid(),
      name: input.name,
      domain: input.domain,
      trustmrr_slug: input.trustmrr_slug ?? null,
      created_at: nowIso(),
      last_refreshed_at: null,
    };
    this.competitors.push(competitor);
    return competitor;
  }

  async deleteCompetitor(id: string): Promise<void> {
    await delay();
    this.competitors = this.competitors.filter((c) => c.id !== id);
    this.events = this.events.filter((e) => e.competitor_id !== id);
    this.revenue = this.revenue.filter((r) => r.competitor_id !== id);
  }

  async refreshCompetitor(id: string): Promise<ChangeEvent[]> {
    await delay(500);
    const competitor = await this.getCompetitor(id);
    competitor.last_refreshed_at = nowIso();
    return this.events
      .filter((e) => e.competitor_id === id)
      .sort((a, b) => b.detected_at.localeCompare(a.detected_at));
  }

  async listChangeEvents(competitorId: string): Promise<ChangeEvent[]> {
    await delay();
    return this.events
      .filter((e) => e.competitor_id === competitorId)
      .sort((a, b) => b.detected_at.localeCompare(a.detected_at));
  }

  async acknowledgeChangeEvent(eventId: string): Promise<ChangeEvent> {
    await delay();
    const e = this.events.find((x) => x.id === eventId);
    if (!e) throw new Error(`Event ${eventId} not found`);
    e.acknowledged = true;
    return e;
  }

  async getRevenueContext(
    competitorId: string
  ): Promise<RevenueContext | null> {
    await delay();
    return this.revenue.find((r) => r.competitor_id === competitorId) ?? null;
  }

  async getLatestBriefing(): Promise<Briefing | null> {
    await delay();
    return this.briefings[this.briefings.length - 1] ?? null;
  }

  async generateBriefing(): Promise<Briefing> {
    await delay(500);
    const weekStart = new Date();
    weekStart.setDate(weekStart.getDate() - weekStart.getDay());
    weekStart.setHours(0, 0, 0, 0);

    const sevenDaysAgo = daysAgoIso(7);
    const candidates = this.events
      .filter((e) => !e.acknowledged && e.detected_at >= sevenDaysAgo)
      .sort((a, b) => {
        const rank = { high: 0, medium: 1, low: 2 } as const;
        if (rank[a.severity] !== rank[b.severity]) {
          return rank[a.severity] - rank[b.severity];
        }
        return b.detected_at.localeCompare(a.detected_at);
      });

    const top = candidates.slice(0, 10);
    const competitorsInvolved = new Set(top.map((e) => e.competitor_id)).size;
    const summary =
      top.length === 0
        ? "No changes this week."
        : `Week of ${weekStart.toISOString().slice(0, 10)}: ${
            top.length
          } changes across ${competitorsInvolved} competitors. Top: ${
            top[0].diff_summary
          }`;

    const briefing: Briefing = {
      id: uuid(),
      week_start: weekStart.toISOString(),
      summary_text: summary,
      top_events: top,
      created_at: nowIso(),
    };
    this.briefings.push(briefing);
    return briefing;
  }
}