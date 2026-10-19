const DOMAIN_RE = /^([a-z0-9-]+\.)+[a-z]{2,}$/i;

export function isValidDomain(domain: string): boolean {
  return DOMAIN_RE.test(domain.trim());
}