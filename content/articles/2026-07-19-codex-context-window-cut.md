---
title: "Codex Context Window Cut to 272K: What OpenAI Rolled Back"
slug: "codex-context-window-cut"
date: 2026-07-19
hub: ai-tools
tags: [openai, codex, coding-agents, context-window]
description: "OpenAI cut Codex's default context from 372K back to 272K tokens, matching its own pricing cliff. What changed, why, and how Claude and Gemini compare."
hero_alt: "Illustration of a code editor with a context gauge being dialed down from 372K to 272K tokens"
keyword: "codex context window"
original_value: "Reconciles Codex's new 272K default with GPT-5.6 Sol's advertised 1.05M window using the PR diff and OpenAI's own pricing docs, and adds the Gemini pricing parallel plus an India cost angle no current coverage has."
sources:
  - {title: "PR #33972: Backport refreshed bundled model metadata to 0.144 — openai/codex", url: "https://github.com/openai/codex/pull/33972", primary: true}
  - {title: "PR #34009: Narrow 0.144 hotfix to GPT-5.6 prompts and context — openai/codex", url: "https://github.com/openai/codex/pull/34009", primary: true}
  - {title: "GPT-5.6 Sol model reference — OpenAI", url: "https://developers.openai.com/api/docs/models/gpt-5.6-sol", primary: true}
  - {title: "Codex pricing — OpenAI", url: "https://developers.openai.com/codex/pricing", primary: true}
  - {title: "Thibault Sottiaux (OpenAI Codex engineering lead) on X", url: "https://x.com/thsottiaux/status/2076495156757577895", primary: true}
  - {title: "Context windows — Anthropic documentation", url: "https://platform.claude.com/docs/en/build-with-claude/context-windows", primary: true}
  - {title: "Pricing — Anthropic documentation", url: "https://platform.claude.com/docs/en/about-claude/pricing", primary: true}
  - {title: "Gemini API pricing — Google", url: "https://ai.google.dev/gemini-api/docs/pricing", primary: true}
  - {title: "Octoverse 2025 — GitHub", url: "https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/", primary: true}
  - {title: "Issue #32806: GPT-5.6 Sol context cut despite advertised 1.05M — openai/codex", url: "https://github.com/openai/codex/issues/32806"}
  - {title: "Issue #32486: Default GPT-5.6 context can cross the 272K higher-usage threshold — openai/codex", url: "https://github.com/openai/codex/issues/32486"}
  - {title: "HN discussion: OpenAI reduces Codex model context size", url: "https://news.ycombinator.com/item?id=48965850"}
faq:
  - {q: "What is a context window in an AI coding tool?", a: "It is the amount of text — code, instructions, and conversation — the model can consider at once, measured in tokens (a token is roughly three-quarters of an English word). When a session exceeds it, tools like Codex compress older material into a summary, a process called compaction, which can lose detail on large projects."}
  - {q: "Did the Codex model itself get smaller or worse?", a: "No. The change is a product setting, not a model change. OpenAI's model page still lists GPT-5.6 Sol with a 1.05-million-token context window via the API. What moved is the Codex app's default cap, which went from 372K back down to 272K tokens — the exact point where OpenAI's own long-request surcharge begins."}
  - {q: "Can I still use a larger context window in Codex?", a: "Codex exposes a model_context_window setting in its config.toml, and the underlying API accepts far larger requests. But OpenAI's pricing doc says requests beyond 272K input tokens are billed at double the input rate and 1.5 times the output rate for the whole request, so raising the cap can cost disproportionately more or burn subscription quota faster."}
  - {q: "Which coding assistant has the biggest context window right now?", a: "On paper, several vendors market 1M-class windows. Anthropic documents a 1M-token window at flat per-token pricing on its current Claude models, while Google's Gemini Pro models offer 1M tokens but roughly double their price above 200K tokens. Advertised size and affordable, usable size are not the same thing — which is exactly what the Codex change illustrates."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-07-19T23:35:00+05:30"
---

OpenAI has reduced the default context window in Codex, its AI coding agent, from 372,000 back to 272,000 tokens for the GPT-5.6 Sol, Terra, and Luna models. The change shipped quietly on July 18, 2026 through two config updates in the open-source Codex repository, with no changelog entry. It is best understood as a rollback, not a fresh cut: 372K was a short-lived increase that, by OpenAI's own account, was burning through subscribers' usage quotas unexpectedly fast — because it pushed sessions past the exact point where OpenAI's pricing doubles.

## What exactly changed

The change is visible in the open-source Codex repository. [Pull request #33972](https://github.com/openai/codex/pull/33972), merged on July 18 by an OpenAI staff account, updates the bundled model metadata for the stable 0.144 release: `context_window` and `max_context_window` for GPT-5.6 Sol and Terra drop from 372,000 to 272,000 tokens. A companion change, [PR #34009](https://github.com/openai/codex/pull/34009), confirms the 272K cap applies to all three GPT-5.6 variants — Sol, Terra, and Luna. It is a configuration-only change: one file, no model weights touched.

Nothing about it appears in the [official Codex changelog](https://developers.openai.com/codex/changelog), whose latest entry as of this writing is a July 16 release note about command-safety improvements. Users noticed anyway. A [GitHub issue filed July 13](https://github.com/openai/codex/issues/32806) had already flagged the reduction rolling out silently, calling it a regression against an advertised million-token model. By the morning of July 19, the PR diff was on the [Hacker News front page](https://news.ycombinator.com/item?id=48965850), where it drew 189 points and 89 comments.

The reaction split into two camps. Developers on large codebases said the smaller window forces more "compaction" — the lossy summarisation coding agents perform when a session outgrows its context. As commenter [skerit put it](https://news.ycombinator.com/item?id=48967382): "No matter how good compaction is, on some big projects it needs to read a lot of files… when I use Codex a single session has to compact over and over again." Others argued compaction handles it fine and the cut is a sensible cost move — one commenter reported a 9.5-hour unattended Codex session completing without trouble.

## Why OpenAI pulled 372K back

The most useful frame comes from OpenAI's own pricing documentation. The [GPT-5.6 Sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol) states that requests exceeding 272K input tokens are charged at doubled input rates and 1.5× output rates for the complete request. In other words, 272,000 tokens is an official pricing cliff. A default window of 372K meant an ordinary long session could drift roughly 100K tokens past that cliff by default — silently paying the premium, or draining subscription quota at the premium rate. A [user-filed issue from July 11](https://github.com/openai/codex/issues/32486) documented exactly this mechanism a week before OpenAI acted.

OpenAI's Codex engineering lead, Thibault Sottiaux, [addressed the change on X](https://x.com/thsottiaux/status/2076495156757577895), saying it landed alongside inference optimisations that should give Sol subscribers roughly 10% more usage, and framing it as "no nerfing." Developer summaries of [his follow-up post](https://x.com/thsottiaux/status/2076543065045795309) — linked repeatedly in the HN thread — say the 372K rollout was a main source of unexpectedly high usage burn, and that OpenAI intends to restore the larger window once that is fixed. There is still no formal announcement; as of publish time, a staff X thread and two pull requests are the entire paper trail.

The economics behind the cliff are not mysterious. Long contexts are expensive to serve: attention computation grows steeply with sequence length, and the memory a GPU must hold for a session (the KV cache) [scales linearly with every token kept in context](https://melchi.me/posts/kv-cache/). Longer default windows mean fewer concurrent users per GPU. We looked at what those serving costs translate to in rupee terms in our breakdown of [the real cost of running AI](/articles/real-cost-of-running-ai/) — the same arithmetic is what turns a "free" context increase into a quota problem at scale.

## The 1M-token asterisk

Here is the part most coverage misses: GPT-5.6 Sol's advertised context window never changed. OpenAI's [model reference](https://developers.openai.com/api/docs/models/gpt-5.6-sol) still lists 1,050,000 input tokens. What changed is the *product default* in Codex — which now sits exactly on the pricing boundary. The advertised number is what the model accepts via the API if you pay for it; the default is what OpenAI thinks a subscription can sustainably absorb. The July 18 change closed the gap between marketing and metering.

That distinction applies across the industry, and it is why "which model has the biggest context window" is usually the wrong question. The better question is what a long request costs.

## How rivals price long context

| Product / model | Advertised window | Default in coding tool | Long-request pricing |
|---|---|---|---|
| OpenAI GPT-5.6 Sol (Codex) | [1.05M tokens](https://developers.openai.com/api/docs/models/gpt-5.6-sol) | 272K (was 372K) | 2× input, 1.5× output above 272K |
| Anthropic Claude (Opus 4.8, Sonnet 5, etc.) | [1M tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows) | model window applies | [Flat per-token rate at any length](https://platform.claude.com/docs/en/about-claude/pricing) |
| Google Gemini 3.1 Pro Preview | [1M tokens](https://gemini.google/overview/long-context/) | model window applies | [$2→$4 input, $12→$18 output above 200K](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini 2.5 Pro | 1M tokens | model window applies | [$1.25→$2.50 input, $10→$15 output above 200K](https://ai.google.dev/gemini-api/docs/pricing) |

Two of the three major vendors charge a premium once a request crosses a length threshold — Google's Pro-tier Gemini models double input pricing above 200K tokens, the same mechanic OpenAI applies above 272K. Anthropic is currently the outlier: its documentation states a 900K-token request is billed at the same per-token rate as a 9K one. GitHub Copilot, which [offers these same GPT-5.6 and Claude models](https://docs.github.com/en/copilot/reference/ai-models/supported-models), describes million-token windows as applying to "select models," so what Copilot users get depends on the model they pick.

## The India angle

Context-window economics land differently in a market this large and this price-sensitive. India is now the world's second-largest developer base — [21.9 million developers on GitHub, up from 4.5 million in 2020](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/), ranking first globally in open-source contributions, with GitHub projecting 57.5 million by 2030. Codex's [official plans](https://developers.openai.com/codex/pricing) are priced in dollars everywhere: free, $8, $20, and $100-plus tiers. OpenAI has shown it will localise consumer pricing — ChatGPT Go launched India-first at ₹399/month — but there is no rupee pricing for its coding product, so Indian developers and startups pay the same dollar rates as Silicon Valley, with quota burn as the real bill.

For that audience, the rollback is arguably good news in disguise: a default that quietly charged premium rates was worst for exactly the users who cannot shrug off a doubled token bill. The practical playbook for cost-sensitive teams is unchanged — keep sessions lean, let compaction work, and treat anything past 200K tokens as a deliberate, priced decision rather than a default. We track shifts like this across coding agents and assistants in our [AI tools and apps](/topics/ai-tools/) coverage.

## What to watch

Three things will tell us where this settles. First, whether 372K actually returns — Sottiaux's posts suggest it will once the usage-burn problem is fixed; a return would confirm the rollback framing. Second, whether OpenAI starts documenting changes like this formally: a usage-affecting default shipped via a hotfix PR and a staff tweet is a communication pattern developers have now noticed twice in one week. Third, whether Anthropic's flat-rate 1M pricing survives as a competitive lever, or converges toward the tiered model OpenAI and Google share. And in the background, the pressure that makes all of this matter keeps building from below: smaller models that run locally, like the phone-scale [Bonsai 27B](/articles/bonsai-27b-ai-model-phone/), sidestep per-token context economics entirely — every token processed on-device is one nobody meters.
