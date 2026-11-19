#!/usr/bin/env python3
"""The Daily Atlas — one image of the day's world news, 19 November 2026.

The picture next to this script is a broadsheet front page for Thursday
19 November 2026, headed "THE DAILY ATLAS". Where earlier entries for
this competition led with a single story, this page is built around
one big table — "The Day in Twelve Stories" — that sets out the whole
day in twelve rows, each with a headline, the country it happened in
and a two-line summary. A schematic dot map of the world in the
masthead numbers the places to match the table's rows.

The twelve stories: Trump, Xi and Putin meet face to face in Shenzhen
at APEC; the US and Iran exchange fire across Kuwait, Bahrain and the
Strait of Hormuz; Anthropic's $81.3bn IPO, the largest in history,
prices in the United States; the World Court at The Hague rules on
the Rohingya genocide case; Israeli tanks cross Gaza's ceasefire
line; the Crimean Bridge is attacked again; COP31 in Antalya admits
the 1.5°C promise will slip; Federal Reserve minutes lean towards
further rate hikes; Nvidia's board bars Jensen Huang's return;
Voyager 1 reaches one light-day from Earth; France and Czechia fill
their streets with protesters; and Grand Theft Auto VI launches
worldwide.

The page was drawn with PIL by ``render.py`` in this repository and
committed as ``entry.png``. Nothing here is drawn at run time and
nothing touches the network: this program simply hands the stored
picture over, byte for byte, so the file it writes is identical every
time it runs. The picture is a PNG, 1024 by 1024 pixels, well under
the one-mebibyte limit. Only the Python standard library is used.

To try it by hand:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import pathlib
import struct
import sys

PICTURE = "entry.png"
OUTPUT_DIR_VARIABLE = "MAKEFUN_OUTPUT_DIR"
ONE_MEBIBYTE = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def picture_path() -> pathlib.Path:
    """Where the committed front page lives, beside this script."""
    return pathlib.Path(__file__).resolve().parent / PICTURE


def output_path() -> pathlib.Path:
    """Where the grader expects the picture, or an override for local runs."""
    directory = os.environ.get(OUTPUT_DIR_VARIABLE, "/output")
    return pathlib.Path(directory) / PICTURE


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Read the width and height out of a PNG's IHDR chunk.

    The IHDR chunk always follows the 8-byte signature directly, so the
    width and height are the two big-endian words at a fixed offset.
    Anything that does not start with the PNG signature is refused
    rather than guessed at.
    """
    if not data.startswith(PNG_MAGIC):
        raise ValueError("picture does not start with the PNG magic bytes")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("picture has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def read_picture_bytes() -> bytes:
    """Load the stored picture, refusing anything oversized or misshapen."""
    path = picture_path()
    if not path.is_file():
        raise FileNotFoundError(f"committed picture missing: {path}")
    data = path.read_bytes()
    if len(data) > ONE_MEBIBYTE:
        raise ValueError(f"picture is {len(data)} bytes, over the 1 MiB limit")
    width, height = png_dimensions(data)
    if (width, height) != (1024, 1024):
        raise ValueError(f"picture is {width}x{height}, expected 1024x1024")
    return data


def write_picture(data: bytes) -> pathlib.Path:
    """Place the picture at the output path and check the copy matches."""
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise IOError(f"bytes written to {target} do not match the picture")
    return target


def main() -> int:
    try:
        data = read_picture_bytes()
        target = write_picture(data)
    except (FileNotFoundError, ValueError, IOError, OSError) as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
