# Asset Specs

Target outputs produced by `scripts/build_logo_assets.py`.

## Required Deliverables

1. `logos/<name>-logo-1024.png`
2. `logos/<name>-logo-512.png`
3. `logos/<name>-logo-256.png`
4. `favicon/favicon-16x16.png`
5. `favicon/favicon-32x32.png`
6. `favicon/favicon-48x48.png`
7. `favicon/favicon.ico` (contains 16/32/48)
8. `web/apple-touch-icon.png` (180x180)
9. `web/android-chrome-192x192.png`
10. `web/android-chrome-512x512.png`
11. `web/og-image-1200x630.png`
12. `site.webmanifest`

## Acceptance Criteria

- Icon remains recognizable at 16x16.
- No blurry edges at 32x32 and 48x48.
- No embedded text artifacts unless user explicitly asked for text.
- Works on both light and dark backgrounds.
- Master logo is centered and square-safe.

## Notes

- Use transparent background for icon outputs where possible.
- If generation includes a non-transparent background, regenerate with stronger prompt constraints.
- Prefer silhouette-first designs over detail-heavy illustrations.
