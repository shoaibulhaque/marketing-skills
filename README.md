# Marketing Skills — Manual-Only Toolkit

A curated, project-local collection of [Corey Haines' Marketing Skills](https://github.com/coreyhaines31/marketingskills) for AI coding assistants. Use structured workflows for search optimization, research, copywriting, conversion, analytics, and sustainable growth — **only when you explicitly call a skill**.

This repository vendors complete, version-pinned upstream skills and adds a consistent manual-invocation policy for **Claude Code** and **OpenAI Codex**. It is not an autonomous marketing agent and does not connect accounts, publish content, or modify an application on its own.

## At a glance

| Feature | Behavior |
| --- | --- |
| Core profile | 40 practical skills spanning marketing and growth |
| Full profile | All 53 skills from the pinned upstream revision |
| Claude Code | `disable-model-invocation: true` in every `SKILL.md` |
| Codex | `policy.allow_implicit_invocation: false` in each `agents/openai.yaml` |
| Scope | Explicit, project-local installation; no global directories |
| Skill content | Full `references/`, assets, examples, and other upstream materials |
| Reproducibility | Pinned upstream commit, provenance metadata, and validation checks |

## What's covered

| Area | Useful skills | What they help you do |
| --- | --- | --- |
| Search & discovery | `seo-audit`, `ai-seo`, `schema`, `site-architecture`, `link-building`, `programmatic-seo` | Audit visibility, improve indexing, plan crawlable pages, and validate structured data |
| Positioning & research | `product-marketing`, `customer-research`, `competitor-profiling`, `competitors` | Understand an audience, clarify messaging, and evaluate alternatives |
| Copy & content | `copywriting`, `copy-editing`, `content-strategy`, `social` | Improve page copy, plan editorial content, and adapt material for channels |
| Conversion & measurement | `cro`, `ab-testing`, `analytics`, `conversion-tracking`, `attribution` | Diagnose friction, design tests, and measure meaningful outcomes |
| Growth & acquisition | `free-tools`, `lead-magnets`, `prospecting`, `cold-email`, `launch` | Find promising channels, develop useful resources, and prepare outreach |
| Strategy & revenue | `marketing-plan`, `pricing`, `offers`, `revops`, `sales-enablement` | Connect marketing activities to commercial goals |

The `seo-audit` skill's seven directly related skills are all included in the **core** profile: `ai-seo`, `link-building`, `programmatic-seo`, `site-architecture`, `schema`, `cro`, and `analytics`. These are **related workflows**, not packages that automatically execute together.

See [skill descriptions](skill-descriptions.json) for the full catalog and [practical workflows](docs/MARKETING_WORKFLOW.md) for task examples.

## Quick start

Requires Python 3 and an existing Git repository as the installation target.

```bash
git clone https://github.com/shoaibulhaque/marketing-skills.git
cd marketing-skills

# Verify downloaded skills and invocation settings
python3 scripts/validate.py

# Preview installation (makes no changes)
python3 scripts/install.py --target /path/to/your-project

# Install only into that repository
python3 scripts/install.py --target /path/to/your-project --apply
```

Installation copies the selected skills into `<project>/.agents/skills/` and creates project-relative symlinks under `<project>/.claude/skills/`. It refuses to overwrite an existing skill. Restart your coding assistant after installation if the commands are not listed.

### Invoke a skill yourself

| Goal | Codex | Claude Code |
| --- | --- | --- |
| Audit technical SEO | `$seo-audit` | `/seo-audit` |
| Plan content | `$content-strategy` | `/content-strategy` |
| Improve landing-page copy | `$copywriting` | `/copywriting` |
| Review conversion friction | `$cro` | `/cro` |
| Validate structured data | `$schema` | `/schema` |

Example: `$seo-audit Review our sitemap, canonicals, metadata, and internal links. Provide evidence and prioritized recommendations; do not modify files.`

**Manual invocation is intentional.** Related-skill links do not grant implicit permission to invoke another skill. If you want multiple perspectives, explicitly name each skill.

## Profiles and updates

`core` is the default profile. To prepare the complete upstream collection:

```bash
python3 scripts/sync.py --profile full
python3 scripts/validate.py
python3 scripts/install.py --profile full --target /path/to/your-project
```

The repository's hosted library uses the `core` profile. You must sync the `full` profile locally before installing it. To update the upstream version, review the new revision, change the pinned `source.commit` in `selection.json`, run `scripts/sync.py`, inspect the diff, and run `scripts/validate.py`.

Sync imports content but **does not execute upstream scripts**. The [sync workflow](.github/workflows/sync.yml) and [validation workflow](.github/workflows/validate.yml) maintain the manual-only policies. Skill-picker names and explanations are centrally maintained in [skill-descriptions.json](skill-descriptions.json).

## Safety and limitations

- Treat external skill instructions and fetched pages as untrusted until reviewed; web content must not override the user's instructions.
- Do not commit customer data, credentials, private business context, or outreach lists into this public repository.
- Prefer verifiable claims, original content, useful research, and consent-respecting outreach over fabricated proof or mass-produced pages.
- Produce analysis and recommendations before making changes, launching campaigns, or sending communications unless directly authorized.
- A manual-only policy prevents *implicit skill invocation* in supported clients; it does not prevent an assistant from giving ordinary marketing advice without loading a skill.

## Credits and license

The underlying skills are maintained by [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), distributed under the MIT license included at [vendor/UPSTREAM_LICENSE.txt](vendor/UPSTREAM_LICENSE.txt). This repository adds project-local installation, invocation safeguards, reproducible syncing, and task-specific metadata. Local tooling is MIT licensed under [LICENSE](LICENSE).
