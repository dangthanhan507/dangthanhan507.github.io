#!/usr/bin/env python3
"""Reproduce the website portrait using the supplied LinkedIn square framing."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "images/sources/an-dang-speaking.png"
OUTPUT = ROOT / "images/an-dang-profile.webp"
# Pixel coordinates in the 800 × 800 LinkedIn reference: left, top, right, bottom.
# Preserve the supplied framing exactly; the website applies the circular mask.
CROP = (0, 0, 800, 800)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE,
                        help="Source screenshot (default: images/sources/an-dang-speaking.png)")
    parser.add_argument("--output", type=Path, default=OUTPUT,
                        help="Output WebP (default: images/an-dang-profile.webp)")
    parser.add_argument("--crop", type=int, nargs=4, default=CROP,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
                        help="Square crop in source pixels (default: 0 0 800 800; entire reference)")
    parser.add_argument("--preview", type=Path,
                        help="Also save a 192-pixel circular PNG preview on white, matching the website")
    args = parser.parse_args()

    with Image.open(args.source) as source:
        source = ImageOps.exif_transpose(source).convert("RGB")
        left, top, right, bottom = args.crop
        if not (0 <= left < right <= source.width
                and 0 <= top < bottom <= source.height):
            parser.error("--crop must be within the source image")
        if right - left != bottom - top:
            parser.error("--crop must be square")
        portrait = source.crop((left, top, right, bottom))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        portrait.save(args.output, format="WEBP", quality=92, method=6)
        print(f"Saved {args.output} ({portrait.width} × {portrait.height})")

    if args.preview:
        with Image.open(args.output) as portrait:
            mask = Image.new("L", portrait.size, 0)
            ImageDraw.Draw(mask).ellipse(
                (0, 0, portrait.width - 1, portrait.height - 1), fill=255
            )
            preview = Image.new("RGB", portrait.size, "white")
            preview.paste(portrait, (0, 0), mask)
            preview = preview.resize((192, 192), Image.Resampling.LANCZOS)
            args.preview.parent.mkdir(parents=True, exist_ok=True)
            preview.save(args.preview, format="PNG")
            print(f"Saved circular preview to {args.preview}")


if __name__ == "__main__":
    main()
