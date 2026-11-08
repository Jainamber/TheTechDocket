# AI AGENT OPERATING DIRECTIVE — C:\NewStartsNov

## 1. The North Star Law (Blocking Constraint)
Before proposing, accepting, or executing any task, code edit, script, or configuration change in this workspace, you **MUST** read and obey:
👉 **`NORTH_STAR.md`**

### The Supreme Law
> **"We do the actions and ONLY those actions (or changes) which improve the North Star Metric. Else we simply do not do it."**

* **Current Season North Star Metric:** **Number of Visitors per Week (`Weekly Visitors`)** on `thetechdocket.com` (`mytechdocket.com`).
* **Permitted Action Levers:**
  1. **Lever 1: Indexation & Cadence** (Keeping daily publication alive, GSC/IndexNow indexing, fixing crawl bottlenecks)
  2. **Lever 2: Topic Selection & CTR** (High search-demand topics, high-CTR titles, hero crops for Discover)
  3. **Lever 3: External Distribution & Referrals** (Social posts, Reddit/HN value posts, carousel exports)
  4. **Lever 4: Retention & Return Loops** (Newsletter capture, daily docket reading habits, internal links)
  5. **Support Enabler:** Strictly necessary measurement/auth fixes (GA4, GSC, GCP Vertex AI auth)

## 2. Mandatory Pre-Action Impact Check
Every proposed plan or action must explicitly begin with:
```markdown
### North Star Impact Check
1. Target Lever: [Lever 1 | Lever 2 | Lever 3 | Lever 4 | Enabler]
2. Causal Mechanism: [1 sentence explaining how this brings more weekly visitors]
3. Expected Payoff Window: [Immediate | Short-Term | Medium-Term]
4. Verdict: [PROCEED / REJECT]
```
If an action is purely aesthetic, speculative, architectural without visitor impact, or internal-only, you must return **REJECT** and stop.

## 3. The Blacklist
* ❌ NO CSS/styling overhauls or font redesigns without a measured CWV/bounce failure.
* ❌ NO internal CLI/tool proliferation that does not publish or distribute content.
* ❌ NO refactoring working code for cosmetic elegance.
* ❌ NO premature monetization complexity before visitor thresholds are cleared.
