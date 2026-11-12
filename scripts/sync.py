#!/usr/bin/env python3
"""Vendor a pinned subset of Corey Haines' marketing skills; never install globally."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_git(*args: str) -> None:
    subprocess.run(['git', *args], check=True)


def patch_claude_frontmatter(path: Path) -> None:
    content = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', content, re.DOTALL)
    if not match:
        raise ValueError(f'Not a valid SKILL.md with YAML frontmatter: {path}')
    fm = match.group(1)
    if re.search(r'(?m)^disable-model-invocation\s*:', fm):
        fm = re.sub(r'(?m)^disable-model-invocation\s*:\s*[^\n]*',
                    'disable-model-invocation: true', fm)
    else:
        fm = fm.rstrip() + '\ndisable-model-invocation: true'
    if re.search(r'(?m)^user-invocable\s*:', fm):
        fm = re.sub(r'(?m)^user-invocable\s*:\s*[^\n]*',
                    'user-invocable: true', fm)
    content = '---\n' + fm + '\n---\n' + content[match.end():]
    path.write_text(content, encoding='utf-8')


def patch_codex_metadata(path: Path, name: str, descriptions: dict) -> None:
    """Set concise skill-picker descriptions and prevent implicit Codex invocation.

    Keep any additional upstream metadata rather than replacing the whole file.
    """
    info = descriptions[name]
    path.parent.mkdir(parents=True, exist_ok=True)
    src = path.read_text(encoding='utf-8') if path.exists() else ''
    display = json.dumps(info['display_name'], ensure_ascii=False)
    description = json.dumps(info['short_description'], ensure_ascii=False)

    if re.search(r'(?m)^interface:\s*$', src):
        for field, value in [('display_name', display), ('short_description', description)]:
            key_pattern = rf'(?m)^  {field}:.*$'
            if re.search(key_pattern, src):
                src = re.sub(key_pattern, lambda _: f'  {field}: {value}', src)
            else:
                src = re.sub(r'(?m)^interface:\s*$', lambda m: m.group() + f'\n  {field}: {value}', src, count=1)
    else:
        src = (f'interface:\n  display_name: {display}\n'
               f'  short_description: {description}\n' + src)

    if re.search(r'(?m)^policy:\s*$', src):
        if re.search(r'(?m)^  allow_implicit_invocation:', src):
            src = re.sub(r'(?m)^  allow_implicit_invocation:.*$',
                         '  allow_implicit_invocation: false', src)
        else:
            src = re.sub(r'(?m)^policy:\s*$', 'policy:\n  allow_implicit_invocation: false', src, count=1)
    else:
        src = src.rstrip() + '\npolicy:\n  allow_implicit_invocation: false\n'
    path.write_text(src, encoding='utf-8')


def reject_symlinks(folder: Path) -> None:
    for p in folder.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Upstream skill contains symlink: {p}. Review upstream before copying.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['core', 'full'], default='core')
    parser.add_argument('--upstream-dir', type=Path, help='Use a trusted local checkout (useful offline)')
    args = parser.parse_args()

    manifest = json.loads((ROOT / 'selection.json').read_text())
    skills = manifest['profiles'][args.profile]['skills']
    descriptions = json.loads((ROOT / 'skill-descriptions.json').read_text(encoding='utf-8'))
    undefined = sorted(set(skills) - set(descriptions))
    if undefined:
        raise ValueError(f'Missing descriptions for: {undefined}')
    source = manifest['source']
    with tempfile.TemporaryDirectory(prefix='marketing-skills-') as td:
        checkout = args.upstream_dir.resolve() if args.upstream_dir else Path(td) / 'upstream'
        if not args.upstream_dir:
            print(f"Fetching {source['repository']} at {source['commit']}", flush=True)
            run_git('clone', '--quiet', '--no-checkout', source['repository'], str(checkout))
            run_git('-C', str(checkout), 'checkout', '--quiet', '--detach', source['commit'])
        if not (checkout / 'skills').is_dir():
            raise FileNotFoundError(f'Not an upstream Marketing Skills checkout: {checkout}')
        if not args.upstream_dir:
            actual_sha = subprocess.check_output(
                ['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
            if actual_sha != source['commit']:
                raise RuntimeError(f'Expected {source["commit"]}, found {actual_sha}')

        staging = Path(td) / 'vendor-skills'
        staging.mkdir()
        for name in skills:
            original = checkout / 'skills' / name
            if not (original / 'SKILL.md').is_file():
                raise FileNotFoundError(f'Missing upstream skill: {name}')
            reject_symlinks(original)
            dest = staging / name
            shutil.copytree(original, dest)
            patch_claude_frontmatter(dest / 'SKILL.md')
            patch_codex_metadata(dest / 'agents' / 'openai.yaml', name, descriptions)
        # Do not leave a half-updated skill library if the source was incomplete.
        vendor = ROOT / 'vendor'
        vendor.mkdir(exist_ok=True)
        destination = vendor / 'skills'
        old = vendor / '.previous-skills'
        if old.exists():
            shutil.rmtree(old)
        if destination.exists():
            destination.rename(old)
        try:
            shutil.move(str(staging), str(destination))
        except BaseException:
            if old.exists():
                old.rename(destination)
            raise
        if old.exists():
            shutil.rmtree(old)
        license_path = checkout / 'LICENSE'
        if license_path.exists():
            shutil.copyfile(license_path, vendor / 'UPSTREAM_LICENSE.txt')
        provenance = {
            'repository': source['repository'],
            'commit': source['commit'],
            'profile': args.profile,
            'skill_count': len(skills),
            'skills': skills,
            'changes': ['Claude: disable-model-invocation true',
                        'Codex: policy.allow_implicit_invocation false'],
        }
        (vendor / 'PROVENANCE.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Vendored {len(skills)} fully referenced skills into vendor/skills/.')
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'validate.py')], check=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
