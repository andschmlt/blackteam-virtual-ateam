# R-SEO-02: Astro SEO Implementation Standards

**Priority:** P0 Critical
**Enforced Since:** 2026-02-13
**Applies To:** ALL Astro projects (europeangaming.eu, lover.io, northeasttimes.com, Australian Sports Hub, any future Astro site)
**Source:** astro-seo open-source component (https://github.com/jonasmerlin/astro-seo)

---

## MANDATORY: Use `astro-seo` Component

Every Astro project MUST use the `astro-seo` npm package for `<head>` SEO tag management. No manual `<meta>` tag construction in layouts.

### Installation (Required for All Astro Projects)

```bash
npm install astro-seo
# or
pnpm add astro-seo
```

### Import Pattern (ALWAYS)

```astro
---
import { SEO } from "astro-seo";
---
```

---

## Rule Checklist (MANDATORY on Every Page)

### R-SEO-02a: Title Management

- [ ] `title` prop set on every page (50-60 characters, include target keyword)
- [ ] `titleTemplate` set in shared layout (e.g., `"%s | Site Name"`)
- [ ] `titleDefault` set as fallback in layout

```astro
<SEO
  title="Page-Specific Title With Keywords"
  titleTemplate="%s | Paradise Media"
  titleDefault="Paradise Media - iGaming Intelligence"
/>
```

### R-SEO-02b: Meta Description

- [ ] `description` prop set on every page (150-160 characters)
- [ ] Description includes primary keyword naturally
- [ ] No duplicate descriptions across pages

### R-SEO-02c: Canonical URL

- [ ] `canonical` prop set OR auto-generated from `Astro.site` config
- [ ] `Astro.site` configured in `astro.config.mjs` (REQUIRED for auto-canonical)
- [ ] `removeTrailingSlashForRoot` set to match site's `trailingSlash` config
- [ ] No duplicate canonical URLs across different pages

### R-SEO-02d: Robots Meta

- [ ] Default: `index, follow` (astro-seo default)
- [ ] `noindex={true}` on non-indexable pages (Coming Soon, admin, staging)
- [ ] `nofollow={true}` where appropriate
- [ ] **CRITICAL:** noindexed pages MUST be excluded from sitemap (learned from ASH conflict)
- [ ] Use `robotsExtras` for advanced directives: `"max-snippet:-1, max-image-preview:large"`

### R-SEO-02e: Open Graph Tags (REQUIRED on Every Public Page)

- [ ] `openGraph.basic.title` set (can differ from page title — more descriptive for social)
- [ ] `openGraph.basic.type` set (`"website"` for pages, `"article"` for articles/posts)
- [ ] `openGraph.basic.image` set (1200x630px recommended)
- [ ] `openGraph.basic.url` set or auto-generated
- [ ] `openGraph.image.alt` set (accessibility — astro-seo warns if missing)
- [ ] `openGraph.image.width` and `openGraph.image.height` set (1200, 630)
- [ ] `openGraph.optional.description` set
- [ ] `openGraph.optional.siteName` set

**For Articles:**
- [ ] `openGraph.article.publishedTime` set (ISO 8601)
- [ ] `openGraph.article.modifiedTime` set (ISO 8601)
- [ ] `openGraph.article.authors` set
- [ ] `openGraph.article.section` set
- [ ] `openGraph.article.tags` set

### R-SEO-02f: Twitter Cards (REQUIRED on Every Public Page)

- [ ] `twitter.card` set (`"summary_large_image"` preferred)
- [ ] `twitter.site` set (site's Twitter handle)
- [ ] `twitter.title` set
- [ ] `twitter.description` set
- [ ] `twitter.image` set (same as OG image or Twitter-optimized)
- [ ] `twitter.imageAlt` set

### R-SEO-02g: Language Alternates (When Applicable)

- [ ] `languageAlternates` array set for multilingual sites
- [ ] Includes `x-default` entry for fallback language
- [ ] Uses correct ISO 639-1 / ISO 3166-1 codes (e.g., `en-US`, `pt-BR`)

### R-SEO-02h: Extended Tags

- [ ] `extend.link` used for preconnect, dns-prefetch, apple-touch-icon
- [ ] `extend.meta` used for theme-color, fb:app_id if applicable
- [ ] No manual `<meta>` or `<link>` tags outside of astro-seo component

---

## Reference Implementation (Layout Template)

```astro
---
// src/layouts/Layout.astro
import { SEO } from "astro-seo";

interface Props {
  title: string;
  description: string;
  image?: string;
  article?: {
    publishedTime: string;
    modifiedTime?: string;
    authors?: string[];
    section?: string;
    tags?: string[];
  };
  noindex?: boolean;
}

const {
  title,
  description,
  image = "/default-og-image.jpg",
  article,
  noindex = false,
} = Astro.props;

const canonicalURL = new URL(Astro.url.pathname, Astro.site);
const ogType = article ? "article" : "website";
---

<html lang="en">
  <head>
    <SEO
      title={title}
      titleTemplate="%s | Site Name"
      titleDefault="Site Name - Tagline"
      description={description}
      canonical={canonicalURL}
      noindex={noindex}
      nofollow={noindex}
      openGraph={{
        basic: {
          title: title,
          type: ogType,
          image: new URL(image, Astro.site).toString(),
          url: canonicalURL.toString(),
        },
        optional: {
          description: description,
          siteName: "Site Name",
          locale: "en_US",
        },
        image: {
          width: 1200,
          height: 630,
          alt: title,
          type: "image/jpeg",
        },
        ...(article && {
          article: {
            publishedTime: article.publishedTime,
            modifiedTime: article.modifiedTime,
            authors: article.authors,
            section: article.section,
            tags: article.tags,
          },
        }),
      }}
      twitter={{
        card: "summary_large_image",
        site: "@site_handle",
        title: title,
        description: description,
        image: new URL(image, Astro.site).toString(),
        imageAlt: title,
      }}
      extend={{
        link: [
          { rel: "icon", href: "/favicon.ico" },
          { rel: "sitemap", href: "/sitemap-index.xml" },
        ],
        meta: [
          { name: "theme-color", content: "#ffffff" },
        ],
      }}
    />
    <slot name="head" />
  </head>
  <body>
    <slot />
  </body>
</html>
```

---

## What astro-seo Does NOT Cover (Handle Separately)

These features require manual implementation alongside astro-seo:

| Feature | Solution | Owner |
|---------|----------|-------|
| JSON-LD Structured Data | Manual `<script type="application/ld+json">` in `<Fragment slot="head">` | B-WALT |
| XML Sitemap | Custom `sitemap.xml.ts` (NOT @astrojs/sitemap — causes conflicts) | B-WALT |
| RSS Feed | `@astrojs/rss` or custom endpoint | B-WALT |
| Breadcrumb Schema | JSON-LD in page template | B-WALT |
| Multiple OG Images | Not supported — use single best image | B-RANK |
| robots.txt | Static file or Astro endpoint | B-WALT |

---

## Validation Checklist (W-LARS / W-EVAN Enforcement)

Before any Astro page goes to production, validate:

1. **astro-seo installed?** Check `package.json` for `"astro-seo"` dependency
2. **SEO component imported?** Every layout must import from `"astro-seo"`
3. **Title present?** 50-60 chars, keyword-rich
4. **Description present?** 150-160 chars
5. **Canonical URL consistent?** No duplicates, matches site config
6. **OG tags complete?** basic.title + basic.type + basic.image + image.alt
7. **Twitter card present?** card + site + title + description + image
8. **Robots directive correct?** noindex pages excluded from sitemap
9. **No raw `<meta>` tags?** All meta handled through astro-seo component
10. **JSON-LD separate?** Structured data in `<Fragment slot="head">`, not in astro-seo

---

## astro-seo TypeScript Interface (Quick Reference)

```typescript
interface SEOProps {
  title?: string;
  titleTemplate?: string;       // "%s | My Site"
  titleDefault?: string;
  charset?: string;
  description?: string;
  canonical?: URL | string;
  removeTrailingSlashForRoot?: boolean;
  noindex?: boolean;
  nofollow?: boolean;
  noarchive?: boolean;
  nocache?: boolean;
  robotsExtras?: string;       // "max-snippet:-1, max-image-preview:large"
  languageAlternates?: Array<{ href: URL | string; hrefLang: string }>;
  openGraph?: {
    basic: { title: string; type: string; image: string; url?: URL | string };
    optional?: {
      audio?: string;
      description?: string;
      determiner?: string;
      locale?: string;
      localeAlternate?: string[];
      siteName?: string;
      video?: string;
    };
    image?: {
      url?: URL | string;
      secureUrl?: URL | string;
      type?: string;
      width?: number;
      height?: number;
      alt?: string;
    };
    article?: {
      publishedTime?: string;
      modifiedTime?: string;
      expirationTime?: string;
      authors?: string[];
      section?: string;
      tags?: string[];
    };
  };
  twitter?: {
    card?: "summary" | "summary_large_image" | "app" | "player";
    site?: string;
    creator?: string;
    title?: string;
    description?: string;
    image?: URL | string;
    imageAlt?: string;
  };
  extend?: {
    link?: Partial<HTMLLinkElement>[];
    meta?: Partial<HTMLMetaElement & { property: string }>[];
  };
  surpressWarnings?: boolean;   // Note: typo is in the actual package
}
```

---

## Enforcement

- **B-WALT** (SEO White Hat Analyst): Implements astro-seo in all Astro projects
- **B-RANK** (SEO Commander): Audits OG/social sharing quality across sites
- **B-SAM** (SEO Manager): Ensures team follows these standards
- **W-EVAN** (SEO White Hat Validator): Validates compliance against this checklist
- **W-LUNA** (SEO Commander Validator): Final SEO approval includes astro-seo check
- **W-LARS** (SEO Compliance): Verifies astro-seo rules on every deployment

**Failure to comply = DEPLOYMENT BLOCKED (same as R-SEC-01)**

---

---

## Cross-Reference: R-SEO-03 Technical SEO Rules

For technical SEO requirements beyond `astro-seo` component usage, see **R-SEO-03** at `~/.claude/standards/ASTRO_TECHNICAL_SEO_RULES.md`.

R-SEO-03 covers:
- **R-SEO-03a:** Trailing slash configuration (`trailingSlash` in astro.config.mjs)
- **R-SEO-03b:** External image hotlinking ban (self-host all images)
- **R-SEO-03c:** Title length budget (metaTitle + suffix <= 60 chars)
- **R-SEO-03d:** Meta description coverage (every page type)
- **R-SEO-03e:** OG type differentiation (article vs website)
- **R-SEO-03f:** Navigation link budget (max 20 direct links per nav section)
- **R-SEO-03g:** Schema.org consistency (SportsTeam, Person, NewsArticle)
- **R-SEO-03h:** Sitemap-build parity (filters must match)
- **R-SEO-03i:** Thin content mitigation (< 200 words = enrich or noindex)

---

*Rule R-SEO-02 | Created 2026-02-13 | Source: astro-seo v1.1.0*
*Approved by: B-BOB (BlackTeam Director) + W-WOL (WhiteTeam Director)*
