# Repository maintenance instructions

This repository maintains a reusable, pinned collection of marketing skills with explicit invocation policies. Treat the upstream skill text as third-party material; do not silently change its intended workflows or execute copied scripts.

- Keep the library independent of any particular company, website, client, repository, or technology stack.
- Do not invoke marketing skills unless the user explicitly names the skill.
- Preserve `disable-model-invocation: true` in every vendored `SKILL.md` frontmatter.
- Preserve `policy.allow_implicit_invocation: false` in every vendored `agents/openai.yaml`.
- Describe each skill accurately and distinctively in `skill-descriptions.json`, and keep generated Codex metadata consistent.
- Preserve complete upstream skill directories, the upstream license, and pinned provenance.
- Keep installation project-scoped; never write to global agent directories or application source.
- Run `python3 scripts/validate.py` after changes, and report missing references or profile gaps.
