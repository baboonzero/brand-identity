#!/usr/bin/env python3
"""Export favicon and logo assets from a master PNG logo."""

from __future__ import annotations

import argparse
import json
import pathlib

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required. Install with: python -m pip install pillow") from exc


def center_square(image: Image.Image) -> Image.Image:
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def save_resized(image: Image.Image, out_path: pathlib.Path, size: int) -> None:
    resized = image.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(out_path, format="PNG")


def create_web_manifest(out_dir: pathlib.Path, product_name: str) -> None:
    manifest = {
        "name": product_name,
        "short_name": product_name,
        "icons": [
            {"src": "web/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "web/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone",
    }
    (out_dir / "site.webmanifest").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True), encoding="utf-8"
    )


def create_og_image(logo_square: Image.Image, out_path: pathlib.Path) -> None:
    canvas = Image.new("RGBA", (1200, 630), (255, 255, 255, 255))
    logo = logo_square.resize((420, 420), Image.Resampling.LANCZOS)
    x = (1200 - logo.width) // 2
    y = (630 - logo.height) // 2
    canvas.alpha_composite(logo, (x, y))
    canvas.convert("RGB").save(out_path, format="PNG")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Master logo PNG path.")
    parser.add_argument("--name", required=True, help="Product name used in filenames and manifest.")
    parser.add_argument("--output-dir", required=True, help="Destination directory.")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output_dir).resolve()
    logos_dir = out_dir / "logos"
    favicon_dir = out_dir / "favicon"
    web_dir = out_dir / "web"

    logos_dir.mkdir(parents=True, exist_ok=True)
    favicon_dir.mkdir(parents=True, exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as image:
        rgba = image.convert("RGBA")
        square = center_square(rgba)

    safe_name = args.name.strip().lower().replace(" ", "-")
    for size in (1024, 512, 256):
        save_resized(square, logos_dir / f"{safe_name}-logo-{size}.png", size)

    for size in (16, 32, 48):
        save_resized(square, favicon_dir / f"favicon-{size}x{size}.png", size)

    ico_base = square.resize((512, 512), Image.Resampling.LANCZOS)
    ico_base.save(favicon_dir / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    save_resized(square, web_dir / "apple-touch-icon.png", 180)
    save_resized(square, web_dir / "android-chrome-192x192.png", 192)
    save_resized(square, web_dir / "android-chrome-512x512.png", 512)
    create_og_image(square, web_dir / "og-image-1200x630.png")
    create_web_manifest(out_dir, args.name)

    print(f"[OK] Exported assets to {out_dir}")


if __name__ == "__main__":
    main()
