# SignalStack — Design System

This file is the single source of truth for UI decisions. Any agent doing
UI work must read this first. Do not invent new tokens, colors, or
spacing values. If something is missing, add it here before using it.

The design intent is "calm intelligence terminal": dense, readable,
low-chrome, built for scanning. Think linear.app meets a trading terminal,
not a marketing landing page.

## Principles

1. **Signal over decoration.** No gradients, no illustrations, no hero
   sections. Every pixel carries information.
2. **Density with breathing room.** Tables and lists are compact, but
   sections are separated by generous whitespace.
3. **One accent color.** Used only for interactive elements and severity
   "high". Everything else is neutral.
4. **Monospace for data.** Numbers, timestamps, domains, and diffs are
   monospace. Prose is sans-serif.

## Color tokens

Define these as CSS variables in `frontend/src/styles/tokens.css`.

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0e1116` | App background |
| `--surface` | `#161b22` | Cards, panels, table rows |
| `--surface-raised` | `#1f2630` | Hover, active row, popovers |
| `--border` | `#2a313c` | Dividers, card borders |
| `--text` | `#e6edf3` | Primary text |
| `--text-muted` | `#8b949e` | Secondary text, labels, timestamps |
| `--accent` | `#4f8cff` | Links, primary buttons, focus rings |
| `--accent-muted` | `#1f3a66` | Accent button hover |
| `--severity-low` | `#3fb950` | Low severity badge |
| `--severity-medium` | `#d29922` | Medium severity badge |
| `--severity-high` | `#f85149` | High severity badge |
| `--success` | `#3fb950` | Verified badge, positive growth |
| `--danger` | `#f85149` | Errors, negative growth |

Dark theme only for MVP. Do not add a light theme toggle.

## Typography

| Role | Font | Size | Weight | Line height |
|------|------|------|--------|-------------|
| Body | Inter, system-ui, sans-serif | 14px | 400 | 1.5 |
| Label | Inter, system-ui, sans-serif | 12px | 500 | 1.4 |
| Heading 1 | Inter, system-ui, sans-serif | 24px | 600 | 1.3 |
| Heading 2 | Inter, system-ui, sans-serif | 18px | 600 | 1.3 |
| Data | JetBrains Mono, ui-monospace, monospace | 13px | 400 | 1.5 |
| Data emphasis | JetBrains Mono, ui-monospace, monospace | 13px | 600 | 1.5 |

Uppercase labels (e.g. "MRR", "LAST REFRESHED") use `letter-spacing: 0.04em`
and `--text-muted`.

## Spacing scale

Use only these values: `4px, 8px, 12px, 16px, 24px, 32px, 48px`.

- Card padding: `16px`
- Section gap: `24px`
- Table row height: `40px`
- Inline gap between icon and text: `8px`

## Radius and elevation

- Border radius: `6px` for cards and inputs, `4px` for badges.
- No drop shadows. Use `--border` and `--surface-raised` for hierarchy.

## Layout

- Fixed left sidebar, `240px` wide, `--surface` background.
- Top bar, `56px` tall, contains the page title and primary action.
- Main content area, max width `1100px`, centered, `24px` padding.
- Sidebar items: icon + label, `40px` tall, active item uses
  `--surface-raised` and a `2px` left border in `--accent`.

## Components

### Button

- Primary: `--accent` background, white text, `6px` radius, `8px 16px`
  padding. Hover: `--accent-muted`.
- Secondary: transparent background, `--border` border, `--text` text.
- Danger: `--danger` background, white text. Used only for delete.
- Disabled: 40% opacity, no hover.
- Never use icon-only buttons without an `aria-label`.

### Badge (severity)

- Pill shape, `4px` radius, `2px 8px` padding, 12px label font.
- `low` → `--severity-low` text on transparent background with
  `--severity-low` border.
- `medium` → `--severity-medium` text on transparent background with
  `--severity-medium` border.
- `high` → `--severity-high` background, white text. High is the only
  filled badge, so it draws the eye.

### Badge (verified)

- "Verified via TrustMRR" → `--success` text, `--success` border,
  transparent background. Prefixed with a small check icon.

### Card

- `--surface` background, `1px solid --border`, `6px` radius, `16px`
  padding.
- Card title: Heading 2, `--text`.
- Card meta (e.g. "Last refreshed"): Label, `--text-muted`.

### Table

- Header row: Label style, uppercase, `--text-muted`, `--border` bottom.
- Body rows: `40px` height, `--border` bottom, hover → `--surface-raised`.
- Numeric cells right-aligned, monospace.
- Domain cells monospace, `--accent` on hover, clickable.

### Diff viewer

- Monospace, `13px`, `--surface` background, `--border`.
- Added lines: `--success` text, no background.
- Removed lines: `--danger` text, no background.
- Context lines: `--text-muted`.
- Line numbers in a `48px` gutter, `--text-muted`.

### Empty state

- Centered in the content area, max width `360px`.
- One sentence in `--text-muted`, one primary button below.
- No illustrations. Optional single icon in `--text-muted`.

### Loading state

- Skeleton rows using `--surface-raised` with a subtle pulse animation.
- Never use a full-page spinner. Skeletons match the shape of the final
  content.

### Toast

- Bottom-right, `--surface-raised` background, `--border`, `6px` radius,
  `12px 16px` padding.
- Auto-dismiss after 4 seconds. Success and error variants use the
  `--success` / `--danger` accent on the left border only.

## Page structure rules

- Every page has exactly one Heading 1 in the top bar.
- Every page has at most one primary button in the top bar.
- Destructive actions (delete competitor) require a confirmation dialog.
- The competitor detail page uses tabs: `Changes`, `Revenue`, `Briefing`.
  Tabs are text-only, active tab has a `2px` `--accent` underline.

## Accessibility

- All interactive elements must be keyboard reachable.
- Focus ring: `2px` `--accent`, `2px` offset.
- Color is never the only signal: severity badges also carry text.
- Minimum contrast ratio 4.5:1 for body text.

## What not to do

- No emoji in the UI.
- No gradients.
- No rounded corners larger than `6px`.
- No marketing copy ("Supercharge your workflow!"). Labels are literal.
- No icon libraries beyond a single set (Lucide) to keep weight down.