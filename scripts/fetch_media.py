#!/usr/bin/env python3
"""Fetch unmodified project media from the versioned source manifest."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "media-sources.json")
    parser.add_argument("--record-hashes", action="store_true",
                        help="Record checksums for newly added manifest entries")
    parser.add_argument("--verify", action="store_true",
                        help="Check local files only, without downloading")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    for asset in manifest["assets"]:
        path = (ROOT / asset["path"]).resolve()
        if not path.is_relative_to(ROOT):
            parser.error(f"Path outside repository: {asset['path']}")
        if args.verify or path.exists():
            data = path.read_bytes()
        else:
            request = Request(asset["url"], headers={"User-Agent": "AnDangAcademicSite/1.0"})
            with urlopen(request, timeout=60) as response:
                data = response.read()
        checksum = hashlib.sha256(data).hexdigest()
        if asset.get("sha256") and asset["sha256"] != checksum:
            raise ValueError(f"Checksum mismatch: {asset['path']}")
        if not asset.get("sha256"):
            if not args.record_hashes:
                parser.error(f"Missing checksum: {asset['path']}; use --record-hashes on first import")
            asset["sha256"] = checksum
        if not args.verify:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        print(f"Verified {asset['path']} ({len(data):,} bytes)")
    if args.record_hashes:
        args.manifest.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
