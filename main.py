#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261122 bounty,
"Sum up 22 November's world news in one image".

Writes the committed entry.png to /output/entry.png. The image is a
one-page front page of the world news of Sunday 22 November 2026,
compiled from wire reports published that day.

The write is atomic: the PNG lands on a temporary file in /output
first, is flushed and fsynced, then os.replace() moves it onto the
final path, so a reader never sees a half-written file. Afterwards
the result is read back and verified byte-for-byte against the
source (length + sha256); any mismatch exits non-zero.

Standard library only, no network. Deterministic: the program runs
twice and both runs write the same bytes.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
TMP = "/output/.entry.png.tmp"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(SRC, "rb") as fin, open(TMP, "wb") as fout:
        fout.write(fin.read())
        fout.flush()
        os.fsync(fout.fileno())
    os.replace(TMP, DST)
    src_hash, dst_hash = sha256_of(SRC), sha256_of(DST)
    if src_hash != dst_hash or os.path.getsize(SRC) != os.path.getsize(DST):
        print(f"verification failed: src sha256 {src_hash} != dst {dst_hash}",
              file=sys.stderr)
        return 1
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes, sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
