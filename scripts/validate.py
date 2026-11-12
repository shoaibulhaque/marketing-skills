#!/usr/bin/env python3
"""Check that every vendored skill is manual-only in both Codex and Claude Code."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / 'selection.json').read_text())
    vendor = ROOT / 'vendor' / 'skills'
    if not vendor.is_dir():
        print('ERROR: no vendored skills; first run scripts/sync.py', file=sys.stderr)
        return 2
    found = sorted(x.name for x in vendor.iterdir() if x.is_dir())
    errors = []
    expected = sorted(manifest['profiles']['steeric']['skills'])
    if set(found) != set(expected) and set(found) != set(manifest['profiles']['full']['skills']):
        errors.append('Vendored skills do not match either declared profile')
    for name in found:
        directory = vendor / name
        f = directory / 'SKILL.md'
        c = directory / 'agents' / 'openai.yaml'
        if not f.exists():
            errors.append(f'{name}: missing SKILL.md'); continue
        s = f.read_text(encoding='utf-8')
        m = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', s, re.DOTALL)
        if not m:
            errors.append(f'{name}: malformed YAML frontmatter'); continue
        front = m.group(1)
        if not re.search(r'(?m)^disable-model-invocation:\s*true\s*$', front):
            errors.append(f'{name}: Claude automatic invocation not disabled')
        if not c.exists() or not re.search(r'(?m)^  allow_implicit_invocation:\s*false\s*$', c.read_text(encoding='utf-8')):
            errors.append(f'{name}: Codex implicit invocation not disabled')
        # Check relative references only; external URLs are intentionally omitted.
        for match in re.finditer(r'\]\(((?:\.?\.?/)?references/[^)#\s]+(?:\.md|\.json))\)', s):
            relative = match.group(1)
            if not (directory / relative).resolve().is_file():
                errors.append(f'{name}: missing reference {relative}')
    missing_seo = set(manifest['seo_audit_related']) - set(found)
    if missing_seo:
        errors.append('Missing direct SEO related skills: ' + ', '.join(sorted(missing_seo)))
    for problem in errors:
        print('ERROR:', problem, file=sys.stderr)
    if errors:
        return 1
    print(f'PASS: {len(found)} skills, both invocation guards, references, SEO-related skills')
    return 0


if __name__ == '__main__':
    sys.exit(main())
