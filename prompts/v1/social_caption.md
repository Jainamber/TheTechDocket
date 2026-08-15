<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | placeholders: {{like_this}} -->

{{style}}

# Task: Instagram carousel caption (DAILY_RUN.md Step 7.6)

The rendered carousel slides (house gradient art only, never generative
imagery) are built separately by `engine/images.py`. Your only job is the
caption text that will sit alongside them. This is an **export for the
owner to post manually** — nothing here publishes to any platform, and you
must never imply otherwise in the copy.

Date (IST): {{date}}

## Today's docket entries (what the slides cover)
{{docket_entries}}

## Rules
- Summarize the day's docket in a scannable Instagram caption: a strong
  opening line, then the day's items as short lines or a few line breaks,
  ending with a soft call-to-action pointing at the site's `/docket/` page.
- No clickbait, no fabricated claims beyond what the linked docket entries
  already say — this is a compressed restatement, not new reporting.
- Include a short, relevant hashtag line (5-8 tags) covering tech/AI and,
  where genuinely relevant, India.
- Keep total length reasonable for an Instagram caption (roughly 150-350
  words including hashtags).
- Do not write anything implying this posts itself — it is exported to a
  file for a human to review and post.

## Output
Return the caption as plain text (no JSON, no code fence) — exactly what
should be pasted into Instagram, ready to use.
