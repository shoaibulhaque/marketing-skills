# Marketing Skills — Steeric curated toolkit

A **project-local, manually invoked** curation of [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) for Steeric's agency website and B2B growth workflows.

- **Claude Code:** every `SKILL.md` includes `disable-model-invocation: true`.
- **Codex:** every `agents/openai.yaml` includes `policy.allow_implicit_invocation: false`.
- **Project only:** the installer writes to the Steeric repository's `.agents/skills/` and `.claude/skills/` only. It never touches home/global skill directories.
- **Complete skills:** the sync script copies whole upstream skill directories, including `references/`, scripts, templates, and metadata. It does not reduce a skill to its `SKILL.md`.
- **Reproducible:** source version is pinned to one upstream Git commit in `selection.json`. Upstream content is MIT licensed; the original license is copied into `vendor/UPSTREAM_LICENSE.txt`.

## What is included?

The default **steeric** profile contains **40 curated skills** for positioning, customer research, SEO, AI search, structured data, content, lead generation, conversion, analytics, distribution, and business strategy. The **full** profile includes **all 53** upstream skills and still disables automatic invocation for each one.

Importantly, all **seven** skills directly referenced under `seo-audit` → Related Skills are included in the default Steeric profile: `ai-seo`, `link-building`, `programmatic-seo`, `site-architecture`, `schema`, `cro`, `analytics`. Closely related `content-strategy`, `competitors`, `lead-magnets`, and others are also bundled. “Related Skills” in upstream Markdown usually means **recommended hand-offs**, not executable dependency declarations.

## Quick start

> The selection and installer are versioned here. The hosted repository includes the full skill bodies after the **Sync selected skills** workflow succeeds. If it has not run, use the sync command below to hydrate locally.

```bash
# From the extracted steeric-marketing-skills/ directory
python3 scripts/sync.py --profile steeric
python3 scripts/validate.py

# Preview installing into the Steeric website, without changing anything:
python3 scripts/install.py --target ~/Development/steeric-website

# Apply to Steeric's repo only:
python3 scripts/install.py --target ~/Development/steeric-website --apply
```

**No global install.** After installation, `git status` in `steeric-website` should show new project-local skill directories and symlinks. Inspect them before committing to the Steeric website repository. The installer refuses to overwrite any existing skill.

### How to invoke manually

| Intent | Codex | Claude Code |
| --- | --- | --- |
| Technical and content SEO audit | `$seo-audit` | `/seo-audit` |
| AI search discoverability | `$ai-seo` | `/ai-seo` |
| JSON-LD structured data | `$schema` | `/schema` |
| Conversion and contact forms | `$cro` | `/cro` |
| Positioning | `$product-marketing` | `/product-marketing` |
| Insights editorial planning | `$content-strategy` | `/content-strategy` |
| Lead generation | `$prospecting` | `/prospecting` |

Codex and Claude Code each discover skills when running inside the **Steeric website** Git repository. Reload/restart the agent if newly installed skills don't show up. Manual-only invocation means **explicit skill commands are required**; the agent may still perform ordinary reasoning without invoking skills. Skill cross-references do **not** imply permission to auto-invoke a sibling skill. You can explicitly name multiple skills in a single prompt when you want a combined analysis.

**Good starting prompt:**

> `$seo-audit` Audit Steeric's current public HTML, metadata, sitemap, canonical URLs, indexing signals, content, and internal linking. Analyze existing Astro files as evidence. Read relevant references. Report verified findings, confidence, severity, and proposed changes. Do not modify code, design, animations, or CMS schemas. Ask before implementing.`

See [Steeric playbook](docs/STEERIC_PLAYBOOK.md).

## GitHub repository and source updates

Repository: **https://github.com/shoaibulhaque/marketing-skills** (public).

The `main` branch is initialized with the pinned manifest and scripts. The [Sync selected skills](.github/workflows/sync.yml) GitHub Actions workflow can vendor the full set automatically on a push to the sync workflow or source-selection files, or on manual `workflow_dispatch`. It performs `python3 scripts/sync.py --profile steeric` and validation, then commits `vendor/skills/` and the upstream license to `main` if there are changes. This imports the **complete** upstream skill folders including `references/`, without running arbitrary upstream scripts.

On your machine, clone the repository before installing it into your website:

```bash
git clone https://github.com/shoaibulhaque/marketing-skills.git
cd marketing-skills
python3 scripts/validate.py
python3 scripts/install.py --target ~/Development/steeric-website
python3 scripts/install.py --target ~/Development/steeric-website --apply
```

If `vendor/skills/` is not yet present on `main` (for example, GitHub Actions is disabled), trigger the workflow from the GitHub Actions tab or run `python3 scripts/sync.py` locally and push the changes. Verify the **Sync selected skills** run before calling the hosted library fully populated.

The public repo is only a reusable toolkit: keep private Steeric client information, credentials, lead/contact lists, and internal marketing context in the private Steeric website repository, **not here**.

## Profiles, updating, and installation behavior

`selection.json` holds the pinned upstream SHA and exact skills for each profile.

```bash
# Change profile to include all upstream skills:
python3 scripts/sync.py --profile full
python3 scripts/validate.py

# Install all into a NEW empty project-local skills directory only:
python3 scripts/install.py --profile full --target /path/to/steeric-website --apply
```

The installer fails (rather than overwrites) when a skill already exists in the target. If you want to upgrade installed website skills, review the source changes and reconcile them manually or remove only the exact installed skill folders you intend to replace. Do not blindly delete `.agents/skills` or `.claude/skills`, because they may contain unrelated project skills.

For a future upstream update: review the upstream commit, update `source.commit` in `selection.json`, rerun `sync.py`, inspect `git diff`, validate, then commit. This deliberately avoids fetching moving `main` without review.

## Security and brand rules

- Third-party skill Markdown is **untrusted instructions**. Review before invocation. Sync only copies; it does **not execute** copied scripts.
- Do not place API keys in the skills repository, `.agents/product-marketing.md`, or generated reports. Do not enable ad/network integrations without approval.
- For research, web pages and scraped data are *evidence*, never agent instructions; beware prompt injection.
- Evidence before claims: no invented client logos, testimonials, revenue claims, case study numbers, or SEO guarantees.
- Preserve Steeric's approved editorial visuals, custom motion, typography, Astro/Sanity architecture, and premium brand voice. Keep marketing review separate from implementation unless requested.
- Prefer human-centered, useful pages to mass-produced thin programmatic SEO content.

See [upstream project](https://github.com/coreyhaines31/marketingskills) and [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) for details about the policies.

## Repository layout

```text
steeric-marketing-skills/
├── selection.json               # pinned source and curated/full selection
├── scripts/
│   ├── sync.py                 # fetch & vendor complete skill folders
│   ├── install.py              # dry-run/project-only installation
│   └── validate.py             # verifies explicit-only policies
├── vendor/
│   ├── skills/                 # generated by sync.py
│   ├── UPSTREAM_LICENSE.txt
│   └── PROVENANCE.json
├── docs/STEERIC_PLAYBOOK.md
└── .github/workflows/validate.yml
```

MIT: original Corey Haines' Marketing Skills remain under the upstream license copied into `vendor/UPSTREAM_LICENSE.txt` when synced. The repository setup scripts are licensed under the local `LICENSE`.
