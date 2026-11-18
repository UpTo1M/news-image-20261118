"""Entry point for the news-image-20261118 competition.

Generates the 1024x1024 front-page image with PIL (see draw.py) and writes
it to <output_dir>/entry.png, where output_dir comes from the
MAKEFUN_OUTPUT_DIR environment variable (default "/output"). The bot
directory is mounted read-only by the grader, so this script never writes
to it. Deterministic: same input always produces the same bytes. No
network, no randomness, no timestamps.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from draw import build_image  # noqa: E402


def main():
    img = build_image()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
