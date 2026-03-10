# R-CSS-01: No :global() in Imported CSS Files

**Priority:** P1 High
**Created:** 2026-02-25
**Applies To:** All Astro projects using CSS imports

---

## Rule

NEVER use `:global()` wrappers in standalone `.css` files. They are only valid inside Astro `<style>` blocks.

---

## Background

`:global()` wrappers in `globals.css` caused broken list indentation across 19 pages on australiafootball.com. The `.prose ul/ol/li` rules were wrapped with `:global()` in `globals.css`, which was imported via `@import` inside `<style is:global>`. Astro does NOT strip `:global()` from `@import`ed files — browsers received literal `:global(.prose ul)` which is invalid CSS.

---

## Rules

### 1. Standalone `.css` files — NEVER use `:global()`

```css
/* WRONG - globals.css */
:global(.prose ul) { ... }
:global(.prose ol) { ... }

/* CORRECT - globals.css */
.prose ul { ... }
.prose ol { ... }
```

Files imported via `@import` in `<style is:global>` are **already global** — no wrappers needed.

### 2. Scoped `<style>` blocks in `.astro` — `:global()` IS valid

```astro
<!-- CORRECT - [slug].astro -->
<style>
  .prose :global(h2) { ... }
  .prose :global(ul) { ... }
</style>
```

This is the correct Astro pattern for targeting child elements within a scoped component.

### 3. `<style is:global>` blocks — NO `:global()` needed

```astro
<!-- CORRECT -->
<style is:global>
  .prose h2 { ... }
</style>

<!-- WRONG -->
<style is:global>
  :global(.prose h2) { ... }
</style>
```

The `is:global` attribute already makes all rules global.

---

## Post-Change Verification

After ANY CSS change, verify the built output:

```bash
# Build the site
npm run build

# Check for :global() leaks in built CSS
grep ":global" dist/_astro/*.css

# Expected: no matches
# If matches found: FAIL — fix source CSS
```

---

## Impact

**19 pages** depend on `globals.css` for `.prose` styling:
- News articles
- 13 team profile pages
- 3 player profile pages

Only betting + casino pages have their own scoped `.prose` rules as safety net.

---

## Enforcement

| System | How Enforced |
|--------|-------------|
| `/seo_audit_engine` | R-CSS-01 validation phase |
| Ralph Loops QA | Visual check on built pages |
| WhiteTeam W-MAYA | CSS review |
| Build pipeline | Post-build grep check |

---

**Version:** 1.0.0
