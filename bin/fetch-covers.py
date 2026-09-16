#!/usr/bin/env python3
"""Scarica le copertine remote di un catalogo in _media/ e riscrive il campo
`cover:` con il path relativo servito da imgix.

Uso: bin/fetch-covers.py [_data/books.yml ...]

Idempotente: le cover gia' locali (senza schema http) vengono saltate.
"""
import mimetypes
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "_media"
UA = "Mozilla/5.0 (compatible; alorenzi.eu cover fetcher)"


def slugify(text, fallback):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60].strip("-")
    return text or fallback


def download(url, dest_dir, slug):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
        ext = mimetypes.guess_extension(resp.headers.get_content_type()) or ".jpg"
    if ext == ".jpe":
        ext = ".jpg"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug}{ext}"
    dest.write_bytes(body)
    return dest, len(body)


def process(data_file):
    data_file = Path(data_file)
    subdir = data_file.stem  # books.yml -> books
    lines = data_file.read_text(encoding="utf-8").splitlines(keepends=True)

    title, used, changed = "", set(), 0
    for i, line in enumerate(lines):
        m = re.match(r"- title: (.*)$", line)
        if m:
            raw = m.group(1).strip()
            if len(raw) > 1 and raw[0] in "'\"" and raw[-1] == raw[0]:
                raw = raw[1:-1].replace(raw[0] * 2, raw[0])
            title = raw
            continue

        m = re.match(r"(\s*cover: )(\S.*)$", line)
        if not m or "://" not in m.group(2):
            continue

        url = m.group(2).strip().strip("'\"")
        slug = base = slugify(title, f"cover-{i}")
        n = 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)

        try:
            dest, size = download(url, MEDIA / subdir, slug)
        except Exception as err:  # rete, 404, host sparito
            print(f"  SKIP {title}: {err}", file=sys.stderr)
            continue

        rel = dest.relative_to(MEDIA)
        lines[i] = f"{m.group(1)}{rel}\n"
        changed += 1
        print(f"  {rel} ({size // 1024} KB) <- {url}")

    if changed:
        data_file.write_text("".join(lines), encoding="utf-8")
    print(f"{data_file}: {changed} copertine scaricate")


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["_data/books.yml"]:
        process(ROOT / arg if not Path(arg).is_absolute() else arg)
