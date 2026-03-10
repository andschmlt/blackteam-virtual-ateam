# R-IMG-01: Google Image Optimization Standards

**Priority:** P0 Critical
**Enforced Since:** 2026-02-22
**Applies To:** ALL content-generating commands (`/bedrock_agent`, `/news_update_agent`, `/content_palm`) and ALL Astro projects
**Source:** Google Image SEO Best Practices + Core Web Vitals Requirements

---

## Purpose

Optimizing images requires tight partnership between the **developer** (B-TECH, B-CODY, B-MAX) who builds and implements, and the **SEO analyst** (B-RANK, B-WALT) who strategizes and audits. When both follow these rules, the result is:
- Blazing-fast page loads (great for Core Web Vitals)
- Highly indexed, context-rich visuals (great for Google Images and organic search)

---

## Part 1: Developer Rules (B-TECH, B-CODY, B-MAX)

The developer's goal: deliver images as fast and efficiently as possible without breaking layout or relying on the main JavaScript thread.

### DO's (MANDATORY)

#### R-IMG-01a: Use Next-Gen Formats
- Serve images in **WebP or AVIF** (30-50% better compression than JPEG/PNG)
- Provide fallbacks using `<picture>` tag for older browsers:
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="descriptive alt text" width="800" height="600">
</picture>
```

#### R-IMG-01b: Set Explicit Dimensions
- **ALWAYS** include `width` and `height` attributes on `<img>` tags
- This reserves DOM space before load, preventing **Cumulative Layout Shift (CLS)**
```html
<!-- CORRECT -->
<img src="hero.webp" alt="..." width="800" height="600">

<!-- WRONG - causes CLS -->
<img src="hero.webp" alt="...">
```

#### R-IMG-01c: Use Responsive Images
- Implement `srcset` and `sizes` so the browser downloads the appropriate size per viewport
```html
<img
  srcset="image-400w.webp 400w, image-800w.webp 800w, image-1200w.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1024px) 800px, 1200px"
  src="image-800w.webp"
  alt="descriptive alt text"
  width="800" height="600"
>
```

#### R-IMG-01d: Optimize Largest Contentful Paint (LCP)
- Identify the **hero image** (largest image above the fold)
- Preload it or mark it high-priority so the browser fetches it immediately:
```html
<!-- Option 1: Preload in <head> -->
<link rel="preload" as="image" href="/hero.webp">

<!-- Option 2: fetchpriority attribute -->
<img src="hero.webp" alt="..." fetchpriority="high" width="1200" height="600">
```

#### R-IMG-01e: Implement Native Lazy Loading
- Add `loading="lazy"` to all images **below the fold**
- Defers loading until the user scrolls near them, saving initial bandwidth
```html
<img src="below-fold.webp" alt="..." loading="lazy" width="400" height="300">
```

### DON'Ts (VIOLATIONS BLOCK DEPLOYMENT)

#### R-IMG-01f: NEVER Lazy-Load the LCP Image
- **NEVER** use `loading="lazy"` on the hero image or any image above the fold
- This artificially delays LCP and hurts Core Web Vitals
```html
<!-- WRONG - lazy hero kills LCP -->
<img src="hero.webp" alt="..." loading="lazy">

<!-- CORRECT - hero loads immediately -->
<img src="hero.webp" alt="..." fetchpriority="high" width="1200" height="600">
```

#### R-IMG-01g: NEVER Hide Vital Images in CSS
- Googlebot **does NOT index** images set via `background-image` in CSS
- If an image carries contextual weight or needs to rank, it **MUST** be an HTML `<img>` tag
```css
/* WRONG - invisible to Google */
.hero { background-image: url('hero.webp'); }
```
```html
<!-- CORRECT - indexable by Google -->
<img src="hero.webp" alt="Australian sports betting comparison" width="1200" height="600">
```

#### R-IMG-01h: NEVER Rely on JavaScript for Core Image Rendering
- Do NOT use `data-src` attributes that require JS libraries to swap to `src`
- If JavaScript fails or is delayed, images won't load and Googlebot may miss them
```html
<!-- WRONG - JS dependency -->
<img data-src="image.webp" class="lazy-js">

<!-- CORRECT - native HTML -->
<img src="image.webp" alt="..." loading="lazy" width="400" height="300">
```

---

## Part 2: SEO Analyst Rules (B-RANK, B-WALT, B-SAM)

The SEO analyst's goal: ensure search engine crawlers can easily discover, understand, and index images to maximize keyword relevance and accessibility.

### DO's (MANDATORY)

#### R-IMG-01i: Descriptive Hyphenated File Names
- Rename files **before upload** using natural language, separated by hyphens
```
CORRECT: australia-sports-betting-app.jpg
CORRECT: best-online-casinos-canada-2026.webp
WRONG:   IMG_20260222_001.jpg
WRONG:   hero_image_v3_final.png
```

#### R-IMG-01j: Context-Driven Alt Text
- Alt text must read like a natural sentence describing the image to someone who cannot see it
- Keep **under 125 characters** for screen reader compatibility
- Include relevant keywords naturally
```html
<!-- CORRECT -->
<img alt="A user scrolling through live AFL betting odds on a mobile app" ...>
<img alt="Comparison table of top 5 Canadian online casinos with bonus amounts" ...>

<!-- WRONG - keyword stuffing -->
<img alt="sports betting australia bet now free odds best betting" ...>

<!-- WRONG - starts with "image of" -->
<img alt="Image of a sports betting app" ...>

<!-- WRONG - empty alt on content image -->
<img alt="" ...>
```

#### R-IMG-01k: Place Images Near Relevant Text
- Google uses surrounding text (headings, captions, paragraphs) to understand image context
- Place images directly after the heading or paragraph they relate to
- Use `<figure>` and `<figcaption>` when a caption adds value

#### R-IMG-01l: Audit Core Web Vitals
- Regularly monitor with: Google PageSpeed Insights, Lighthouse, Google Search Console
- **LCP MUST be under 2.5 seconds**
- **CLS MUST be under 0.1**

#### R-IMG-01m: Use Image Sitemaps
- For image-heavy sites, submit a dedicated Image Sitemap via Google Search Console
- Ensures deep-level images are crawled and indexed

### DON'Ts (VIOLATIONS BLOCK DEPLOYMENT)

#### R-IMG-01n: NEVER Keyword-Stuff Alt Text
- Stuffing triggers spam filters and ruins accessibility
- One or two natural keywords maximum per alt attribute

#### R-IMG-01o: NEVER Use "Image of" / "Picture of" Prefix
- Search engines and screen readers already know it's an image
- Wastes the 125-character limit

#### R-IMG-01p: NEVER Leave Alt Attribute Blank on Content Images
- Empty `alt=""` tells screen readers to skip the image
- Only use `alt=""` for purely decorative elements (dividers, background shapes)

#### R-IMG-01q: NEVER Block Image Directories in robots.txt
- Check that `/images/`, `/wp-content/uploads/`, `/assets/` are NOT disallowed
- Run periodic robots.txt audits

---

## Cross-Functional Checklist: SEO & Dev Alignment

| Feature | SEO Analyst Checks For... | Developer Implements... |
|---|---|---|
| **File Names** | Keywords and descriptive language (hyphenated) | CMS config to preserve original file names on upload |
| **Alt Text** | Relevance, accuracy, accessibility (<125 chars) | Strict HTML validation ensuring `alt` attribute exists |
| **Page Speed** | LCP under 2.5s; CLS under 0.1 | WebP/AVIF formats, `srcset`, explicit `width`/`height` |
| **Indexability** | `<img>` tags for important visuals; unblocked in robots.txt | Standard HTML markup instead of CSS backgrounds or JS injection |
| **Load Priority** | Hero images load instantly; lower images load later | `fetchpriority="high"` for hero; `loading="lazy"` for rest |

---

## Astro-Specific Implementation

For Astro projects (which are the primary output of `/bedrock_agent`):

### Image Component Usage
```astro
---
// Use Astro's built-in Image component for automatic optimization
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.webp';
---

<!-- Astro auto-generates srcset, width, height, and format conversion -->
<Image src={heroImage} alt="Descriptive alt text here" />
```

### Hero Image Pattern (LCP Optimized)
```astro
---
import { Image } from 'astro:assets';
import hero from '../assets/hero.webp';
---

<!-- Hero: NO lazy loading, HIGH fetch priority -->
<Image
  src={hero}
  alt="Comprehensive guide to Australian sports betting sites 2026"
  loading="eager"
  fetchpriority="high"
/>
```

### Below-Fold Pattern
```astro
---
import { Image } from 'astro:assets';
import card from '../assets/card-image.webp';
---

<!-- Below fold: lazy loaded -->
<Image
  src={card}
  alt="BetMGM mobile app interface showing live odds"
  loading="lazy"
/>
```

---

## Enforcement

### BlackTeam Owners
| Persona | Responsibility |
|---------|---------------|
| **B-TECH** (Head of Tech) | Image format conversion, `srcset`, `width`/`height`, `fetchpriority`, `loading` |
| **B-CODY** (CodeGuard) | HTML validation — reject any `<img>` missing `alt`, `width`, `height` |
| **B-MAX** (PixelPerfect) | Visual QA — verify images display correctly, no CLS, responsive behavior |
| **B-RANK** (SEO Commander) | Alt text quality, file naming, image sitemap, CWV audit |
| **B-POST** (Head of Post Production) | Final image QA before deployment — all rules verified |

### WhiteTeam Validators
| Persona | Validates |
|---------|-----------|
| **W-LARS** (SEO Compliance) | Alt text, file names, robots.txt, image sitemap |
| **W-MAYA** (Accessibility) | Alt text accessibility, contrast, WCAG compliance |
| **W-FLUX** (Code Security) | No JS-dependent image loading, proper HTML markup |
| **W-ASTR** (Performance) | LCP, CLS, format optimization, lazy loading correctness |
| **W-OSCA** (Production) | Final deployment check — all R-IMG-01 sub-rules pass |

### Deployment Gate
**Failure to comply with any R-IMG-01 sub-rule = DEPLOYMENT BLOCKED**

Same severity as R-SEC-01 (security) and R-SEO-02 (Astro SEO).

---

## Quick Validation Commands

```bash
# Check all <img> tags have alt, width, height in Astro project
grep -rn '<img' src/ | grep -v 'alt=' | head -20   # Missing alt
grep -rn '<img' src/ | grep -v 'width=' | head -20  # Missing width
grep -rn '<img' src/ | grep -v 'height=' | head -20 # Missing height

# Check for CSS background-image on content images
grep -rn 'background-image' src/styles/ | head -20

# Check for data-src JS lazy loading patterns
grep -rn 'data-src' src/ | head -20

# Check robots.txt for blocked image directories
cat public/robots.txt | grep -i 'disallow.*image\|disallow.*upload\|disallow.*asset'
```

---

*Rule R-IMG-01 | Created 2026-02-22 | Source: Google Image SEO Best Practices + Core Web Vitals*
*Approved by: B-BOB (BlackTeam Director) + W-WOL (WhiteTeam Director)*
*Enforced in: /bedrock_agent, /news_update_agent, /content_palm*
