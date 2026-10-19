import type { SignalService } from "./SignalService";
import { MockSignalService } from "./MockSignalService";
import { HttpSignalService } from "./HttpSignalService";

let instance: SignalService | null = null;

export function getSignalService(): SignalService {
  if (!instance) {
    const useMock = import.meta.env.VITE_USE_MOCK === "true";
    instance = useMock ? new MockSignalService() : new HttpSignalService();
  }
  return instance;
}

export function __setSignalServiceForTests(s: SignalService): void {
  instance = s;
}