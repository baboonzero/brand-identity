#!/usr/bin/env python3
"""Generate logo images with Gemini image generation models."""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import pathlib
import time
import urllib.error
import urllib.request

DEFAULT_MODEL = "gemini-3-pro-image-preview"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def parse_prompt_file(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    prompts = [chunk.strip() for chunk in text.split("\n---\n") if chunk.strip()]
    if not prompts:
        raise ValueError(f"No prompts found in {path}. Use '---' between prompt blocks.")
    return prompts


def call_gemini_image_api(
    *,
    api_key: str,
    model: str,
    prompt: str,
    timeout: int,
    retries: int,
) -> tuple[bytes, str]:
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = response.read().decode("utf-8")
                parsed = json.loads(body)
                image_bytes, text_response = extract_image(parsed)
                return image_bytes, text_response
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            sleep_s = min(2 ** attempt, 8)
            time.sleep(sleep_s)

    raise RuntimeError(f"Gemini API request failed after retries: {last_error}") from last_error


def extract_image(payload: dict) -> tuple[bytes, str]:
    candidates = payload.get("candidates", [])
    if not candidates:
        raise ValueError(f"No candidates in Gemini response: {json.dumps(payload)[:500]}")

    text_parts: list[str] = []
    for candidate in candidates:
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if "text" in part:
                text_parts.append(part["text"])
            inline = part.get("inlineData")
            if inline and "data" in inline:
                mime = inline.get("mimeType", "")
                if mime.startswith("image/"):
                    return base64.b64decode(inline["data"]), "\n".join(text_parts).strip()

    raise ValueError(
        "Gemini returned no image. The model may not support image output for this request."
    )


def build_prompt(brief: str, direction_prompt: str) -> str:
    return (
        "Create a professional software product logo icon. "
        "Output only one clean icon-style mark with transparent background. "
        "No words, no letters unless explicitly requested, no watermark, no mockup scene. "
        "High contrast, scalable, and readable at favicon sizes.\n\n"
        f"PROJECT BRIEF:\n{brief}\n\n"
        f"DESIGN DIRECTION:\n{direction_prompt}\n"
    )


def write_json(path: pathlib.Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief-file", required=True, help="Path to brand brief markdown/text file.")
    parser.add_argument(
        "--prompt-file",
        required=True,
        help="Path to prompts file, with prompt blocks separated by a line containing ---.",
    )
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    parser.add_argument(
        "--model",
        default=os.environ.get("GEMINI_MODEL", DEFAULT_MODEL),
        help=f"Gemini model name (default: {DEFAULT_MODEL} or GEMINI_MODEL).",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GEMINI_API_KEY"),
        help="Gemini API key (default: GEMINI_API_KEY env var).",
    )
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout in seconds.")
    parser.add_argument("--retries", type=int, default=2, help="Retry count per prompt.")
    args = parser.parse_args()

    if not args.api_key:
        if os.isatty(0):
            entered = getpass.getpass("Enter Gemini API key (input hidden): ").strip()
            if entered:
                args.api_key = entered
        if not args.api_key:
            raise SystemExit(
                "Missing API key. Set GEMINI_API_KEY, pass --api-key, or run interactively to be prompted."
            )

    brief_path = pathlib.Path(args.brief_file).resolve()
    prompt_path = pathlib.Path(args.prompt_file).resolve()
    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    brief = brief_path.read_text(encoding="utf-8").strip()
    prompts = parse_prompt_file(prompt_path)
    results: list[dict] = []

    for index, direction in enumerate(prompts, start=1):
        full_prompt = build_prompt(brief, direction)
        image_bytes, text_response = call_gemini_image_api(
            api_key=args.api_key,
            model=args.model,
            prompt=full_prompt,
            timeout=args.timeout,
            retries=args.retries,
        )

        file_stem = f"logo-{index:02d}"
        image_path = output_dir / f"{file_stem}.png"
        image_path.write_bytes(image_bytes)

        metadata = {
            "index": index,
            "model": args.model,
            "brief_file": str(brief_path),
            "prompt_file": str(prompt_path),
            "direction_prompt": direction,
            "composed_prompt": full_prompt,
            "response_text": text_response,
            "image_path": str(image_path),
        }
        write_json(output_dir / f"{file_stem}.json", metadata)
        results.append(metadata)
        print(f"[OK] Wrote {image_path}")

    write_json(output_dir / "generation-summary.json", {"count": len(results), "results": results})
    print(f"[OK] Completed {len(results)} logo generations.")


if __name__ == "__main__":
    main()
