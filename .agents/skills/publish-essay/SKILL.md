---
name: publish-essay
description: Publish a new long-form essay on mugdhapradhan.com from a markdown source. Use when the user says they have added or written a new essay, asks to publish/build/put up an essay or blog post, points at a file in thinking/, or asks to link a new essay from the home and thinking pages. Also use for "add this essay to the site", "make a page for this essay", "publish the blog".
metadata:
  version: 1.0.0
---

# Publish an Essay

Turn a markdown essay into a finished page on the site, linked from the home
page and the thinking page, and verified against its source before commit.

## The one rule that matters

**The essay is the author's text. You are doing typography, not editing.**

Every heading and every sentence on the page comes from the markdown. You are
choosing which of the site's display blocks each paragraph goes into. You are
not writing prose, not titling sections, not tightening, not paraphrasing.

This is where it has gone wrong before: an essay was published with invented
chapter titles ("Twenty-five kilos over my head") in place of the author's own
headings ("Tuesday, 21 July. Morning."). The mechanical work was all correct;
the editorial liberty was the defect. `verify.py` exists to catch exactly that.

## Inputs

| | |
|---|---|
| Source | `thinking/<slug>.md` |
| Image | `images/<slug>.<ext>` |
| Output | `thinking/<slug>.html` at `/thinking/<slug>` |

If the source has no `.md` extension, rename it first. `cleanUrls` is on in
`vercel.json`, so an extensionless `thinking/<slug>` sits at the exact URL the
page needs and can shadow it. (`thinking/mirror-to-men` still has this problem.)

## Steps

### 1. Read the source and plan the mapping

Read the markdown end to end before writing anything. Identify:

- The H1 — this is the essay title, used verbatim.
- The section headings — usually `## **Bold**` or a bold `**line**` between
  `---` separators. **These become the chapter titles, word for word.**
- Every other line is a body paragraph.

If the essay has no section headings at all, ask the user how to break it up.
Do not invent headings to fill the template.

### 2. Ask the user (only what cannot be derived)

Ask these together in one pass, with your recommendation first:

- **Category tag** — reuse an existing one if it fits (`Consciousness &
  Spirituality`, `Consciousness & Gender`, `Philosophy of Health`, `Systems &
  Power`, `The Body & Consciousness`), or propose a new one.
- **Card excerpt** — the 1–2 sentence blurb on the home page card. This is site
  copy, so you may write it, but show it for approval.
- **Hero sub-line** — the italic line under the title. This sits in the author's
  voice, so it needs explicit sign-off, or leave it out.
- **Content note** — only if the essay carries something the reader should be
  warned about. Existing essays have none; do not add one unasked.

Derive the rest: date is the current month (`Jul 2026`), read time is
words ÷ 250 rounded (`19 min read`).

### 3. Build the page from the template

Copy `template.html` and fill the placeholders:

`{{TITLE}}` `{{DESCRIPTION}}` `{{SLUG}}` `{{IMAGE}}` `{{HERO_TITLE}}`
`{{HERO_SUB}}` `{{DATE}}` `{{READ_TIME}}` `{{CATEGORY}}` `{{CHAPTER_NAV}}` `{{BODY}}`

`{{HERO_TITLE}}` is the H1 broken over at most two lines, with the closing
phrase in `<em>`:

```html
The Body Keeps<br>The Score. <em>Or Does It?</em>
```

`{{CHAPTER_NAV}}` is one entry per section, plus `opening` first. Labels are
short forms of the author's own headings — the sidebar is `nowrap`, so keep
them to about 20 characters:

```html
  <a href="#section-cave" class="chapter-dot" data-section="section-cave">
    <span class="chapter-dot-label">The Cave</span>
    <span class="chapter-dot-pip"></span>
  </a>
```

### 4. Lay out the body

Structure, in order:

1. `<section id="opening" class="story-opening">` — cover image, then the
   paragraphs before the first heading.
2. For each section: a chapter divider, then
   `<section id="section-x" class="chapter-section">` with a header and blocks.
3. `<div class="story-break">` (three dots), then `<section class="story-closing">`.

Cover image, first thing inside the opening:

```html
<div class="essay-cover-image reveal">
  <img src="../images/<slug>.<ext>" alt="<describe the image>"
       style="width:100%;max-width:900px;display:block;margin:0 auto 3rem;border-radius:4px;opacity:0.92;">
</div>
```

Chapter header — ornament label, then the author's heading verbatim:

```html
<div class="chapter-header reveal">
  <p class="chapter-label">Chapter <span class="chapter-num-small">IV</span></p>
  <h2 class="chapter-title">The cave</h2>
</div>
```

**Block vocabulary.** Put `reveal` on every top-level block.

| Block | Use for |
|---|---|
| `.prose` > `p` | Ordinary paragraphs. The default; most text is this. |
| `.staccato` | A short paragraph with a turn in it. Two `p`, second gets `.gold`. |
| `.pull-quote` | A long, load-bearing paragraph. Bordered, italic. |
| `.centered-pull` | A single hammer line. Use `<br>` to control the break. |
| `.confession` | An admission plus its gloss. Second `p` gets `.muted`. |

Use them sparingly — a wall of pull-quotes reads as noise. Look at
`thinking/the-body-keeps-score.html` for the rhythm.

Close with a `.centered-pull` and a `.story-signature`, both drawn from the
essay's own last lines.

### 5. What you may and may not do to the text

**Allowed (formatting):**

- Split one source paragraph across two display lines, breaking only at a
  sentence boundary the author already wrote.
- Promote a paragraph into a pull-quote, centered-pull, staccato or confession.
- Italicise a phrase for emphasis with `<em>`.
- Insert `<br>` to control where a line wraps.
- Convert quotes and dashes to entities (`&rsquo;` `&ldquo;` `&middot;`).

**Never:**

- Write a heading, a title, or a transition the author did not write.
- Merge two source paragraphs into one block.
- Reorder, reword, trim, expand or "tighten" anything.
- Drop a paragraph because it seems repetitive or awkward.

### 6. Verify — this is a gate, not a formality

```bash
python3 .agents/skills/publish-essay/verify.py <slug>
```

It walks the source and the page in parallel and fails on dropped text,
invented text, or merged paragraphs. **Exit 0 or you do not proceed.** It also
prints every paragraph split and every italicised phrase — report that list to
the user, since those are the liberties you took on their prose.

Then confirm the page actually works: balanced tags, every `chapter-dot`
target resolving to a real section id, and the page rendered in a browser.

### 7. Link it

Essays are numbered in one shared sequence. The new one takes the next number;
any unpublished placeholder card (`href="#"`) shifts down.

- **`index.html`** — add a card to `.essays-grid` in the `#thinking` section,
  matching the shape of the one above it (`reveal reveal-delay-3`).
- **`thinking.html`** — add an `.essay-card` to `.essays-grid` with number, tag,
  title, date and read time. Renumber anything below it.
- **`sitemap.xml`** — add `https://mugdhapradhan.com/thinking/<slug>` at
  `priority 0.7`, next to the other essays.

### 8. Report, then commit if asked

Tell the user: the URL, the metadata you derived, the formatting liberties
`verify.py` listed, and any line on the page that is yours rather than theirs
(typically the hero sub-line and the card excerpt).

Do not commit unless asked. When asked, stage only the essay's own files —
the page, the `.md`, the image, and the three linked files. This repo has no
`.gitignore` and carries unrelated untracked files; never `git add -A`.
