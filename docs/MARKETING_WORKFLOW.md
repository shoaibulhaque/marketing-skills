# Practical guide to manual marketing skills

These workflows support different business types and development stacks. Choose one relevant skill, run a focused audit or planning task, review the result, and only then authorize implementation.

## Picking a skill

| Need | Invoke | Expected output |
| --- | --- | --- |
| Understand buyers and positioning | `product-marketing` + `customer-research` | Reviewed audience profile, value proposition, and evidence gaps |
| Examine technical search readiness | `seo-audit` | Indexability, metadata, performance and content findings with supporting evidence |
| Check JSON-LD or semantic markup | `schema` | Verified schema types, implementation advice, validation checks |
| Improve AI-assisted search discoverability | `ai-seo` | Crawl access, answer usefulness, source quality, and measurement plan |
| Plan useful articles and landing pages | `content-strategy` | Prioritized topic clusters and original-content opportunities |
| Improve existing page copy | `copy-editing` | Carefully scoped edits that retain the original voice |
| Investigate low-converting forms | `cro` | Diagnosed friction, hypotheses, and measurement suggestions |
| Design controlled experiments | `ab-testing` | Hypothesis, metrics, power assumptions, and decision rules |
| Design inbound engineering tools | `free-tools` | A useful tool concept, audience fit, maintenance considerations |
| Qualify prospects | `prospecting` | Source-backed candidates, explicit selection criteria, evidence and caveats |

All seven SEO-related skills (`ai-seo`, `link-building`, `programmatic-seo`, `site-architecture`, `schema`, `cro`, `analytics`) are included in the core collection.

## Recommended workflow

1. **Define the decision.** State the audience, site or campaign, current problem, constraints, and what success would look like.
2. **Explicitly invoke the relevant skill.** Examples: `$seo-audit` in Codex or `/seo-audit` in Claude Code.
3. **Inspect the evidence.** Distinguish verified observations, reasonable inferences, and unknowns; flag missing data rather than inventing facts.
4. **Produce a reviewable deliverable.** Prefer a prioritized audit, example copy, hypothesis list, or execution checklist over unrequested changes.
5. **Request implementation only when intended.** Make changes in a separate scoped step, keep existing design and behavior intact unless a change is requested, and measure outcomes.

## Examples

**Technical SEO:** `$seo-audit Inspect the deployed site and source files for indexing blockers, metadata defects, canonical problems, internal linking, and structured-data opportunities. List evidence and recommended fixes. Do not edit files.`

**Copy review:** `$copy-editing Improve clarity and specificity in this landing page while preserving the original message and voice. Show before/after suggestions; don't alter the page layout.`

**Combined review:** `$seo-audit $schema Audit SEO and JSON-LD together. Separate observed issues from hypotheses. Propose minimal changes and a validation plan.`

**Market research:** `$customer-research Summarize public customer discussions around this product category. Cite sources, label confidence, and note sampling bias.`

## Important boundaries

- `disable-model-invocation: true` prevents Claude Code from choosing the skills by itself.
- `allow_implicit_invocation: false` provides the equivalent Codex policy.
- Cross-references in an explicitly invoked skill are reading suggestions, not permission to automatically invoke sibling skills.
- Vendor content is pinned to a reviewed upstream revision; verify and inspect new revisions before syncing.
- Neither the collection nor its installer requires global installation, advertising accounts, API keys, or production access.

For complete skill descriptions, see [skill-descriptions.json](../skill-descriptions.json). For source provenance, see [selection.json](../selection.json).
