#!/usr/bin/env python3
"""news-image-20261124 — entry for the make.fun bounty
"Sum up 24 November's world news in one image" (news-image-20261124).

The entry image is the dense front page "THE WORLD TODAY — 24 November
2026" (40 stories / 7 sections, lead COP31 collapses without a deal),
already drawn and stored in this repository as entry.png (1024x1024,
187,253 bytes). This program copies it to /output/entry.png.

Standard library only, no network. The grader's pinned Python image
does not ship Pillow, so the entry does not import PIL at all — it
copies the image the repository holds, which is the simplest entry
the bounty rules describe.
"""

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    src = os.path.join(_HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    # Validate the copy: a PNG starts with its 8-byte magic, and the
    # bounty caps the image at 1 MiB and 1024x1024 (this one is 187,253).
    with open(dst, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("copied file is not a PNG", file=sys.stderr)
        return 1
    if size > 1024 * 1024:
        print(f"image {size} bytes exceeds the 1 MiB cap", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
