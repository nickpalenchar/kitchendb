"""
compresses all images in /static/images/* and adds them to 
/static/images/thumbnail/*
"""
from PIL import Image
import os
import sys

def main(overwrite=False):
  for file in os.listdir("../static/images"):
    if file == "thumbnail":
      continue
    if os.path.exists(f"../static/images/{file}") and not overwrite:
      continue

    im = Image.open(f"../static/images/{file}").copy()
    factor = max(im.size) / 256
    im.thumbnail([s // factor for s in im.size])
    im.save(f"../static/images/thumbnail/{file}")

if __name__ == '__main__':
  main(overwrite=len(sys.argv) > 1)
