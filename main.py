"""ai-excited-01 entry: emit the murmuration image to the output directory.

The image shows a starling murmuration twisting into a giant curling
wave above a hilltop at dusk, a tiny lone figure silhouetted on the
summit below. It ships next to this program as entry.png (JPEG bytes
under that name, which the rules allow). The program copies those bytes
unchanged to MAKEFUN_OUTPUT_DIR/entry.png, so the judge sees exactly
the intended image on every run: deterministic, standard library only,
no network, no image processing at runtime.
"""

import hashlib
import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = Path(__file__).resolve().parent / IMAGE_NAME
    if not source.is_file() or source.stat().st_size == 0:
        raise RuntimeError(f"missing or empty bundled image: {source}")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / IMAGE_NAME

    data = source.read_bytes()
    dest.write_bytes(data)

    # A silent partial write would hand the judge a different image, so
    # compare digests before reporting success.
    if _sha256(dest) != _sha256(source):
        raise RuntimeError("output bytes differ from entry.png")

    return 0


if __name__ == "__main__":
    sys.exit(main())
