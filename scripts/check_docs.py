#!/usr/bin/env python3
"""Lint the manual: links, anchors, structure, leftovers.

Standard library only, so it runs anywhere the docs do.

    python3 scripts/check_docs.py            # offline checks (CI gate)
    python3 scripts/check_docs.py --external # also HEAD external links

Exit code 0 = clean, 1 = problems found.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

# e.g. [text](target) or [text](target "title")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
HTML_A_RE = re.compile(r"<a\s+[^>]*href=\"([^\"]+)\"")

PLACEHOLDERS = ("<your-username>", "<username>", "TODO", "FIXME", "TBD", "XXX")


def slug(text: str) -> str:
    """Approximate GitHub's heading anchor: lowercase, drop punctuation,
    spaces -> '-'. CJK characters are kept as-is."""
    text = text.strip().lower()
    text = re.sub(r"`", "", text)
    text = re.sub(r"\*\*|__|\*|_", "", text)
    out = []
    for ch in text:
        if ch in " \t":
            out.append("-")
        elif ch == "-":
            out.append("-")
        elif ch.isalnum():
            cat = unicodedata.category(ch)
            # letters, digits and CJK are kept; punctuation is dropped
            if cat[0] in ("L", "N"):
                out.append(ch)
        # everything else (., :, ?, （）, /, etc.) is dropped
    s = "".join(out)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def iter_markdown():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(files):
            if name.endswith(".md"):
                yield os.path.join(base, name)


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def headings(text):
    """[(level, title, slug)] outside code fences, with duplicate slugs
    disambiguated the way GitHub does it (slug, slug-1, slug-2)."""
    out = []
    seen = {}
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2)
        base = slug(title)
        if base in seen:
            seen[base] += 1
            base = f"{base}-{seen[base]}"
        else:
            seen[base] = 0
        out.append((level, title, base))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", action="store_true",
                    help="also check external http(s) links (needs network)")
    args = ap.parse_args()

    problems = []
    warnings = []
    files = list(iter_markdown())
    anchors = {os.path.abspath(p): {h[2] for h in headings(read(p))} for p in files}

    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        text = read(path)
        h1 = [h for h in headings(text) if h[0] == 1]

        # --- structure -------------------------------------------------
        if not h1:
            problems.append(f"{rel}: no H1")
        elif len(h1) > 1:
            problems.append(f"{rel}: {len(h1)} H1 headings (expected 1)")

        levels = [h[0] for h in headings(text)]
        for a, b in zip(levels, levels[1:]):
            if b > a + 1:
                warnings.append(f"{rel}: heading jumps H{a} -> H{b}")

        # --- code fences balanced --------------------------------------
        if len([l for l in text.splitlines() if FENCE_RE.match(l)]) % 2:
            problems.append(f"{rel}: unbalanced code fence")

        # --- leftovers --------------------------------------------------
        for token in PLACEHOLDERS:
            if token in text:
                problems.append(f"{rel}: placeholder {token!r} left in the text")

        # --- links ------------------------------------------------------
        targets = LINK_RE.findall(text) + [(m, m) for m in HTML_A_RE.findall(text)]
        for _label, target in targets:
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                if target[1:] and target[1:] not in anchors[os.path.abspath(path)]:
                    problems.append(f"{rel}: dead anchor {target}")
                continue
            file_part, _, anchor = target.partition("#")
            dest = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
            if not os.path.exists(dest):
                problems.append(f"{rel}: broken link {target}")
                continue
            if anchor and dest.endswith(".md"):
                if os.path.abspath(dest) not in anchors:
                    anchors[os.path.abspath(dest)] = {h[2] for h in headings(read(dest))}
                if anchor not in anchors[os.path.abspath(dest)]:
                    problems.append(f"{rel}: dead anchor {target}")

        # --- chapter navigation ----------------------------------------
        if rel.startswith("docs/") and not rel.endswith("glossary.md"):
            if "**导航**" not in text:
                warnings.append(f"{rel}: missing 导航 line")
            if "本章小结" not in text:
                warnings.append(f"{rel}: missing 本章小结")

    if args.external:
        problems.extend(check_external(files))
        problems = [p for p in problems if p]

    if warnings:
        print("warnings:")
        for w in warnings:
            print("  ~", w)
    if problems:
        print("problems:")
        for p in problems:
            print("  x", p)
        print(f"\n{len(problems)} problem(s), {len(warnings)} warning(s), {len(files)} files")
        return 1
    print(f"ok: {len(files)} files, {len(warnings)} warning(s)")
    return 0


def check_external(files):
    """Best-effort HEAD check; network failures are reported, not fatal."""
    import urllib.error
    import urllib.request

    out = []
    seen = set()
    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        for _label, target in LINK_RE.findall(read(path)):
            if not target.startswith(("http://", "https://")) or target in seen:
                continue
            seen.add(target)
            req = urllib.request.Request(target, method="HEAD",
                                         headers={"User-Agent": "web3-primer-linkcheck"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status >= 400:
                        out.append(f"{rel}: external {target} -> HTTP {resp.status}")
            except urllib.error.HTTPError as e:
                # 403/405 often mean "HEAD not allowed", not a broken link
                if e.code not in (403, 405, 429):
                    out.append(f"{rel}: external {target} -> HTTP {e.code}")
            except Exception as e:  # noqa: BLE001 - offline/timeout/DNS
                print(f"note: could not check {target}: {e}", file=sys.stderr)
    return out


if __name__ == "__main__":
    sys.exit(main())
