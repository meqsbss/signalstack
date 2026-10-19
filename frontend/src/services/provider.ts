import type { SignalService } from "./SignalService";
import { MockSignalService } from "./MockSignalService";

let instance: SignalService | null = null;

export function getSignalService(): SignalService {
  if (!instance) {
    instance = new MockSignalService();
  }
  return instance;
}

export function __setSignalServiceForTests(s: SignalService): void {
  instance = s;
}