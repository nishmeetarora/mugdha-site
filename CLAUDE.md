# Mugdha Pradhan — Personal Site

## Project Overview
Personal website for Mugdha Pradhan, founder & CEO of iThrive (functional nutrition startup). The site communicates her story, mission, vision, and "The Remembrance Movement" to investors, event curators, and media.

## Tech Stack
- **Static HTML/CSS/JS** — no framework, no build step
- Each page is a standalone `.html` file
- All styles are inline `<style>` blocks within each HTML file
- All scripts are inline `<script>` blocks

## Design System (locked — do not change)
- **Palette:** `--black: #07060a`, `--deep: #0d0b14`, `--charcoal: #161320`, `--gold: #c9984a`, `--gold-light: #e8c07e`, `--cream: #f0e8d8`, `--white: #faf8f4`
- **Also used:** `--gold-dim: rgba(201,152,74,0.15)`, `--amber: #d4803a`, `--muted: rgba(240,232,216,0.45)`, `--border: rgba(201,152,74,0.2)`
- **Fonts:** Cormorant Garamond (headings, quotes), Cinzel (labels, nav, buttons), Jost (body text)
- **Aesthetic:** Dark, luxurious, editorial. Gold accents on near-black backgrounds. Subtle grain overlay, scroll-reveal animations, custom cursor.
- **Spacing/sizing patterns:** Follow the conventions in `index.html` (clamp-based responsive font sizes, rem-based padding)

## Pages Built
- `index.html` — Main landing page (complete). Hero with additive-blending fire canvas, hook section, numbers, mission, credibility bar, audience cards, story teaser, essays grid, closing CTA, footer.
- `story.html` — The Story page (complete)
- `mission.html` — The Mission page (complete)

## Nav Links (consistent across all pages)
```html
<li><a href="story.html">The Story</a></li>
<li><a href="mission.html">The Mission</a></li>
<li><a href="#work">The Work</a></li>
<li><a href="#thinking">The Thinking</a></li>
<li><a href="#contact">Contact</a></li>
```

## Reusable UI Patterns (copy from index.html — do not reinvent)

**Custom cursor** — always include, copy `.cursor` + `.cursor-ring` divs and their JS verbatim.

**Grain overlay** — always include `<div class="grain"></div>` with its CSS animation.

**Nav** — fixed, logo left + links right. Gains `.scrolled` class on scroll (backdrop blur, border-bottom). Copy verbatim and update active link.

**Section tag** — gold Cinzel label with a short gold line after it:
```html
<p class="section-tag">Label Text</p>
```

**Scroll-reveal** — add `.reveal` (and `.reveal-delay-1/2/3`) to any element that should fade up on scroll. The IntersectionObserver JS handles it — copy from index.html.

**Buttons:**
- `.btn-enter` — bordered, gold fill on hover (hero CTA style)
- `.btn-primary` — solid gold fill, black text
- `.btn-secondary` — bordered gold, transparent bg

**Footer** — logo left, italic quote center, social links right. Copy verbatim.

**CSS variables block** — copy the full `:root { }` block from index.html at the top of every page's `<style>`.

## Content
- Full site content lives in a Google Doc; sections will be pasted into chat as we build each page

## Build Conventions
- Use the `frontend-design` skill when creating or significantly modifying any page
- Maintain consistent nav, footer, and visual language across all pages
- Preserve the custom cursor, grain overlay, and scroll-reveal patterns on every page
- Responsive: mobile-first media queries at 768px and 900px breakpoints
- Hero headlines: 2 clean lines max, `clamp`-based font size, `max-width: 1300px` on hero-content
