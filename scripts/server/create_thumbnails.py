"""
compresses all images in /static/images/* and adds them to 
/static/images/thumbnail/*
"""
from PIL import Image
import os
import sys

PROJECT_ROOT = "../.."
IMAGE_DIR = "static/images"


def create(overwrite=False):
    for file in os.listdir(os.path.join(PROJECT_ROOT, IMAGE_DIR)):
        if file == "thumbnail":
            continue
        if (
            os.path.exists(os.path.join(PROJECT_ROOT, IMAGE_DIR, "thumbnail", file))
            and not overwrite
        ):
            continue

        im = Image.open(os.path.join(PROJECT_ROOT, IMAGE_DIR, file)).copy()
        factor = max(im.size) / 256
        im.thumbnail([s // factor for s in im.size])
        im.save(os.path.join(PROJECT_ROOT, IMAGE_DIR, "thumbnail", file))


if __name__ == "__main__":
    create(overwrite=len(sys.argv) > 1)
