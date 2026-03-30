#!/usr/bin/env python3
"""Download Twitter profile avatars for all people in people.yml.

Skips handles that already have a local file. Run this manually or from CI
to populate docs/avatars/ before deploying to gh-pages.
"""
import time
import urllib.request
from pathlib import Path

import yaml

PEOPLE_FILE = Path(__file__).parent.parent / "people.yml"
AVATARS_DIR = Path(__file__).parent.parent / "docs" / "avatars"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIDigestCN/1.0)"}


def main() -> None:
    with open(PEOPLE_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    AVATARS_DIR.mkdir(parents=True, exist_ok=True)

    for person in data.get("people", []):
        handle = person["twitter_handle"]
        out_path = AVATARS_DIR / f"{handle}.jpg"

        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"  skip  @{handle} (already cached)")
            continue

        url = f"https://unavatar.io/twitter/{handle}"
        print(f"  fetch @{handle} ... ", end="", flush=True)
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                content = resp.read()
            out_path.write_bytes(content)
            print(f"OK ({len(content):,} bytes)")
        except Exception as exc:
            print(f"FAILED: {exc}")
        time.sleep(0.4)


if __name__ == "__main__":
    main()
