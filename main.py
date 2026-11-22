#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261122 bounty,
"Sum up 22 November's world news in one image".

Copies the committed entry.png to /output/entry.png. The image is a
one-page front page of the world news of Sunday 22 November 2026,
compiled from wire reports published that day.

Standard library only, no network. Deterministic: the program runs
twice and both runs write the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
