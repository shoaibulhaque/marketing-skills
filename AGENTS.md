# Repository maintenance instructions

This repository maintains a project-scoped copy of independently reviewed marketing skills. Do not change user application code or install skills into global locations.

- Do not invoke a marketing skill unless the human explicitly names it.
- Every vendored `SKILL.md` must include `disable-model-invocation: true` in YAML frontmatter.
- Every vendored `agents/openai.yaml` must include `policy.allow_implicit_invocation: false`.
- Preserve complete upstream skill folder contents and upstream license; pin upstream commit and document provenance.
- Never execute scripts copied from upstream merely because the content was vendored.
- Run `python3 scripts/validate.py` after updates; report missing references and profile gaps.
- Keep project targeting explicit. Never write to `~/.agents`, `~/.claude`, `~/.codex`, or application code.
