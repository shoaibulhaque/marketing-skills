#!/usr/bin/env python3
"""Copy curated skills only into a specified project; default is dry-run."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path, help='Steeric website repository root')
    parser.add_argument('--profile', choices=['steeric', 'full'], default='steeric')
    parser.add_argument('--apply', action='store_true', help='Actually install (otherwise only preview)')
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if not target.is_dir() or not (target / '.git').exists():
        parser.error(f'--target must be an existing Git repository root: {target}')
    if target == ROOT:
        parser.error('Target must be Steeric website, not this skills repository')

    selection = json.loads((ROOT / 'selection.json').read_text())
    skills = selection['profiles'][args.profile]['skills']
    source = ROOT / 'vendor' / 'skills'
    if not source.is_dir():
        parser.error('Skills not vendored; first run python3 scripts/sync.py')
    provenance = json.loads((ROOT / 'vendor' / 'PROVENANCE.json').read_text())
    available = set(provenance['skills'])
    missing = set(skills) - available
    if missing:
        parser.error(f'Profile requires missing skills: {", ".join(sorted(missing))}; run sync --profile full')

    codex_dir = target / '.agents' / 'skills'
    claude_dir = target / '.claude' / 'skills'
    collisions = []
    for name in skills:
        for p in (codex_dir / name, claude_dir / name):
            if p.exists() or p.is_symlink():
                collisions.append(str(p))
    if collisions:
        parser.error('Refusing to overwrite existing skills. Review first:\n' + '\n'.join(collisions))

    print(f'Project: {target}')
    print(f'Profile: {args.profile} ({len(skills)} skills)')
    print('Destination: .agents/skills/ + .claude/skills/ (symlinks)')
    print('No global directories or application source files will be touched.')
    if not args.apply:
        print('DRY RUN: pass --apply when ready.')
        return 0

    codex_dir.mkdir(parents=True, exist_ok=True)
    claude_dir.mkdir(parents=True, exist_ok=True)
    try:
        for name in skills:
            shutil.copytree(source / name, codex_dir / name, symlinks=False)
            # Linux-friendly project-relative link, tracked by Git.
            os.symlink(Path('..') / '..' / '.agents' / 'skills' / name,
                       claude_dir / name, target_is_directory=True)
    except BaseException:
        print('Partial installation possible; inspect added directories.', file=sys.stderr)
        raise
    print(f'Installed {len(skills)} project-local, manually invoked skills.')
    print('Codex: $seo-audit  |  Claude Code: /seo-audit')
    print('No changes were made to AGENTS.md, application source, or deployment config.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
